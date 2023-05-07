import { _converse, api, converse } from '@converse/headless/core';
import { __ } from 'i18n';
const { u } = converse.env;
import { html } from 'lit';
import { transform } from 'lodash-es';
import RecordToolView from './recording_tool'



converse.plugins.add('langex-audio-toolkit', {
  initialize() {
    _converse.RecordToolView = RecordToolView;
    
    // let isRecording = false;

    // function onRecordingClick(recorder) {
    //   if (!isRecording){
    //     isRecording = true;
    //     recorder.start();
    //     console.log(recorder.state);
    //     console.log("recorder started");
    //     return;
    //   }

    //   recorder.stop();
    //   console.log(recorder.state);
    //   console.log("recorder stopped");
    //   // mediaRecorder.requestData();   
    // }

    api.listen.on('getToolbarButtons', (toolbar_el, buttons) => {
      buttons.push(html`<langex-recording-tool class='recording-tool-container'></langex-recording-tool>`);
      return buttons;
    })   
    

    // TODO: Seperate to audio bot package
    function transformAudioBotMsg(richText, options) {
      if (!richText.is_audiobot) return;
      console.log("Audio bot message transformation")
      var parser = new DOMParser();
      richText.addTemplateResult(0, richText.length, html`${parser.parseFromString(richText.toString(), 'text/html').body}`);
    }

    api.listen.on('beforeMessageBodyTransformed', transformAudioBotMsg);
  }
});
