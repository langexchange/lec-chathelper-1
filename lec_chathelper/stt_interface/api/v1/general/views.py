from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes, schema
from rest_framework import status
from rest_framework.parsers import MultiPartParser
import os
import environ
from lec_chathelper.autoschema import AutoDocstringSchema
from .faster_whisper.utils import (
    model_converter as faster_whisper_model_converter,
)
import torch
import whisper
from faster_whisper import WhisperModel
from threading import Lock
from typing import BinaryIO, Union
from whisper import tokenizer
import numpy as np
import ffmpeg
import logging


######## INIT ############
env = environ.Env()
# TODO: Modify this using sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
environ.Env.read_env(os.path.join(BASE_DIR,'env/.dev.env'))
logger = logging.getLogger(__name__)

# Model config
LANGUAGE_CODES=sorted(list(tokenizer.LANGUAGES.keys()))
SAMPLE_RATE = 16000
ASR_MODEL = env("ASR_MODEL")

# Load model
logger.info("Starting loading model: ")
whisper_model_name= ASR_MODEL
faster_whisper_model_path = os.path.join("{}/models".format(os.path.dirname(os.path.abspath(__file__))), whisper_model_name)
faster_whisper_model_converter(whisper_model_name, faster_whisper_model_path)


if torch.cuda.is_available():
    whisper_model = whisper.load_model(whisper_model_name).cuda()
    faster_whisper_model = WhisperModel(faster_whisper_model_path, device="cuda", compute_type="float16")
else:
    whisper_model = whisper.load_model(whisper_model_name)
    faster_whisper_model = WhisperModel(faster_whisper_model_path)
model_lock = Lock()
######## INIT ############


def get_model(method: str = "openai-whisper"):
  if method == "faster-whisper":
      return faster_whisper_model
  return whisper_model


@api_view(['POST'])
@parser_classes([MultiPartParser])
@schema(AutoDocstringSchema())
def transcribe(request,
    # output : Union[str, None] = Query(default="txt", enum=["txt", "vtt", "srt", "tsv", "json"])
):
  """
    post:
      description: Transcribe or translate an audio record
      summary: Transcribe or translate
                  
      requestBody:
        content:
          multipart/form-data:
            schema:
              type: object
              properties:
                audio_file:
                  type: string
                  format: binary
                task:
                  description: Task type
                  type: string
                  enum: ["transcribe", "translate"]
 
                language:
                  description: Language code recorded in audio. See ISO 639-1 Code https://www.loc.gov/standards/iso639-2/php/code_list.php
                  type: string
                  default: en
              required:
                - audio_file
                - task

      responses:
        '200':
          description: Transcript or translate info
          content:
            'application/json': {}
  """
  payload = request.data
  if "task" not in payload or payload["task"] not in ["transcribe", "translate"]:
    return Response({
      "result": "fail",
      "message": "Missing or invalid task field: type enumerate 'transcribe', 'translate'"
    }, status=status.HTTP_400_BAD_REQUEST)
  task = payload["task"]

  if "language" in payload and payload["language"] not in LANGUAGE_CODES:
    return Response({
      "result": "fail",
      "message": "Sorry this language currently is not supported"
    }, status=status.HTTP_400_BAD_REQUEST)
  language = payload["language"] if "language" in payload else None

  if "audio_file" not in payload:
    return Response({
      "result": "fail",
      "message": "Missing audio_file field"
    }, status=status.HTTP_400_BAD_REQUEST)
  
  audio_file = payload["audio_file"]
  method = payload["method"] if "method" in payload else "openai-whisper"
 
  encode = payload["encode"] if "encode" in payload else True

  result = run_asr(audio_file.file, task, language, method, encode)

  return Response({
    "result": "success",
    "message": result,
  }, status=status.HTTP_200_OK)






"""
{
  "text": " Your power is sufficient, I said.",
 "segments": [
    {
      "id": 0, 
      "seek": 0, 
      "start": 0.0, 
      "end": 2.0, 
      "text": " Your power is sufficient, I said.", 
      "tokens": [50364, 2260, 1347, 307, 11563, 11, 286, 848, 13, 50464], 
      "temperature": 0.0, 
      "avg_logprob": -0.38865739648992365, 
      "compression_ratio": 0.8048780487804879, 
      "no_speech_prob": 0.062102749943733215
    }
  ], 
  "language": "en"
}
"""
def run_asr(
    file: BinaryIO, 
    task: Union[str, None], 
    language: Union[str, None],
    method: Union[str, None],
    encode=True
):
    audio = load_audio(file, encode)
    options_dict = {"task" : task}
    if language:
        options_dict["language"] = language    
    with model_lock:   
        model = get_model(method)
        if method == "faster-whisper":
            segments = []
            text = ""
            i = 0
            segment_generator, info = model.transcribe(audio, beam_size=5, **options_dict)
            for segment in segment_generator:
                segments.append(segment)
                text = text + segment.text
            result = {
                "language": options_dict.get("language", info.language),
                "segments": segments,
                "text": text,
            }
        else:
            result = model.transcribe(audio, **options_dict)

    return result


def load_audio(file: BinaryIO, encode=True, sr: int = SAMPLE_RATE):
    """
    Open an audio file object and read as mono waveform, resampling as necessary.
    Modified from https://github.com/openai/whisper/blob/main/whisper/audio.py to accept a file object
    Parameters
    ----------
    file: BinaryIO
        The audio file like object
    encode: Boolean
        If true, encode audio stream to WAV before sending to whisper
    sr: int
        The sample rate to resample the audio if necessary
    Returns
    -------
    A NumPy array containing the audio waveform, in float32 dtype.
    """
    if encode:
        try:
            # This launches a subprocess to decode audio while down-mixing and resampling as necessary.
            # Requires the ffmpeg CLI and `ffmpeg-python` package to be installed.
            out, _ = (
                ffmpeg.input("pipe:", threads=0)
                .output("-", format="s16le", acodec="pcm_s16le", ac=1, ar=sr)
                .run(cmd="ffmpeg", capture_stdout=True, capture_stderr=True, input=file.read())
            )
        except ffmpeg.Error as e:
            raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}") from e
    else:
        out = file.read()

    return np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0