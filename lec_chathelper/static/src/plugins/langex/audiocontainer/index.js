import { _converse, api, converse } from '@converse/headless/core';
import { __ } from 'i18n';
const { u } = converse.env;
import { html } from 'lit';
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
      buttons.push(html`<langex-recording-tool></langex-recording-tool>`);
      return buttons;
    })   
  }
});
