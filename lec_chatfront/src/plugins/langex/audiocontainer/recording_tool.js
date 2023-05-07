import tplRecordingTool from './templates/recording_tool';
import { ElementView } from '@converse/skeletor/src/element';
// // import { __ } from 'i18n';
import { _converse, api, converse } from "@converse/headless/core.js";
// // import { prefixMentions } from '@converse/headless/utils/core.js';

// const { u } = converse.env;

import './styles/recording_tool.scss'


export default class RecordToolView extends ElementView {

  events = {
    'click .toggle-recording': 'recordingButtonClicked',
    'click .stop-recording': 'stopButtonClicked',
    'click .delete': 'askBeforeRemoveAudioContainer',
  };
    
  async connectedCallback () {
    super.connectedCallback();
    this.isRecording = false;
    this.recorder = null;
    this.mediaStream = null;
    this.chunks = [];
    this.audioFile = null;
    

    //Visualize
    this.audioCtx = new AudioContext();
    this.analyser = this.audioCtx.createAnalyser();
    this.analyser.fftSize = 2048;
    this.bufferLength = this.analyser.frequencyBinCount;
    this.frequencyArray = new Uint8Array(this.bufferLength);
    this.mediaStreamNode = null;
    this.canvasCtx = null;
    this.render();

    //Listen if the audio file is send
    document.addEventListener("audioFileSended", this.removeAudioContainer.bind(this));
  }

  toHTML(){
    return tplRecordingTool();
  }

  removeAudioContainer(){
    const audio_container = this.querySelector("article");
    this.audioFile = null;
    audio_container.remove();

    this.dispatchEvent(new CustomEvent("audioStateChange", { 'detail': {
      state: "clear"
    }, 'bubbles': true,}));
  }

  createFileComponent(){
    const clipContainer = document.createElement("article");
    clipContainer.style.display = "flex";
    clipContainer.style.alignItems = "flex-end";
    const audio = document.createElement('audio');
    audio.style.maxHeight = '22px'
    const deleteButton = document.createElement('button');
    deleteButton.textContent = "Delete";
    deleteButton.className = 'btn btn-danger btn-sm py-0 ml-2 mt-0 delete';
    clipContainer.appendChild(audio);
    clipContainer.appendChild(deleteButton)

    const audioURL = window.URL.createObjectURL(this.audioFile);
    audio.src = audioURL;
    audio.controls = true;

    this.appendChild(clipContainer);
  }

  askBeforeRemoveAudioContainer(e, message = "Are you sure you want to remove the audio"){
    const confirmation = confirm(message)
    if(!confirmation){
      return;
    }
    this.removeAudioContainer();
  }

  initRecorder(stream){
    if(this.audioFile){
      this.askBeforeRemoveAudioContainer(null, "There is the file that is not sent yet ? Do you want to record the new one ?"); 
    }

    this.mediaStream = stream;
    this.recorder = new MediaRecorder(stream, {mimeType: 'audio/webm;codecs="opus"'});

    // Visualization
    this.querySelector('.record-graph').style.display = "inline-block";
    this.mediaStreamNode = this.audioCtx.createMediaStreamSource(stream);
    this.mediaStreamNode.connect(this.analyser);
    this.drawCanvas()
    

    this.recorder.ondataavailable = (function(e) {
      this.chunks.push(e.data);
    }).bind(this)

    this.recorder.onstop = (function(e) {
      const blob = new Blob(this.chunks, { 'type' : 'audio/webm' });
      this.audioFile = new File([blob], "name.webm", {lastModified: new Date(), type:"audio/webm"});
      this.chunks = [];
      this.releaseResources()
      // TODO: Create some thing after creating file.

      this.dispatchEvent(new CustomEvent("audioStateChange", { 'detail': {
        file: this.audioFile,
        state: "stop"
      }, 'bubbles': true,}));
      console.log("recorder stopped");
      
      this.querySelector('.record-graph').style.display = "none";
      this.createFileComponent();
    }).bind(this)

    this.recorder.start()
    this.isRecording = true;

    this.dispatchEvent(new CustomEvent("audioStateChange", { 'detail': {
      state: "recording"
    }, 'bubbles': true,}));
  }

  onGetMediaError(){
    // TODO: Add notifications indicate browser does not support recording here
  }

  releaseResources(){
    this.mediaStream.getTracks().forEach(track => track.stop());
    this.mediaStreamNode.disconnect();
    this.recorder = null;
    this.mediaStream = null;
    this.mediaStreamNode = null;
  }

  stopButtonClicked(){
    const confirmation = confirm("Are you sure you want to stop the recording ?");
    if(!confirmation)
      return;
    this.recorder.stop()  //This will automatically records the file as defined in init function
  }

  recordingButtonClicked(){
    if(!navigator.mediaDevices.getUserMedia){
      onGetMediaError()
    }

    if(this.mediaStream && this.isRecording){
      this.recorder.pause()
      this.isRecording = false;
      return;
    }

    if(this.mediaStream && !this.isRecording){
      this.recorder.resume()
      this.isRecording = true;
      this.dispatchEvent(new CustomEvent("audioStateChange", { 'detail': {
        state: "recording"
      }, 'bubbles': true,}));
      return;
    }

    const constraints =  {audio: true};
    navigator.mediaDevices.getUserMedia(constraints).then(this.initRecorder.bind(this), this.onGetMediaError);
  }

  drawCanvas(){
    const canvas = this.querySelector("canvas");
    const WIDTH = canvas.width
    const HEIGHT = canvas.height;

    requestAnimationFrame(this.drawCanvas.bind(this));

    this.analyser.getByteTimeDomainData(this.frequencyArray);
    const canvasCtx = canvas.getContext("2d");
    canvasCtx.fillStyle = 'rgb(200, 200, 200)';
    canvasCtx.fillRect(0, 0, WIDTH, HEIGHT);
    canvasCtx.lineWidth = 2;
    canvasCtx.strokeStyle = 'rgb(0, 0, 0)';
    canvasCtx.beginPath();

    let sliceWidth = WIDTH * 1.0 / this.bufferLength;
    let x = 0;

    for(let i = 0; i < this.bufferLength; i++) {
      let v = this.frequencyArray[i] / 128.0;
      let y = v * HEIGHT/2;
      if(i === 0) {
        canvasCtx.moveTo(x, y);
      } else {
        canvasCtx.lineTo(x, y);
      }
      x += sliceWidth;
    }

    canvasCtx.lineTo(canvas.width, canvas.height/2);
    canvasCtx.stroke();
  }
  

}

api.elements.define('langex-recording-tool', RecordToolView);
