import { __ } from 'i18n';
import { html } from 'lit';

export default () => {
  const color = 'chat-toolbar-btn-color';
  const i18n_start_call = __('Start a recording');
  return html`
        <button class="toggle-recording" title="${i18n_start_call}">
            <converse-icon color="var(--chat-toolbar-btn-color)" class="fa fa-microphone" size="1em"></converse-icon>
        </button>
        <div class="record-graph">
            <canvas class="visualizer"></canvas>
            <button class="stop-recording m-0" title="${i18n_start_call}">
                <converse-icon color="var(--error-color)" class="fa fa-stop" size="1em"></converse-icon>
            </button>
        </div>
    `;
};
