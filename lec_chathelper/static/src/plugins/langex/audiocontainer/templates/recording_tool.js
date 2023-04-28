import { __ } from 'i18n';
import { html } from 'lit';

export default () => {
  const color = 'chat-toolbar-btn-color';
  const i18n_start_call = __('Start a recording');
  return html`
      <button class="toggle-recording" title="${i18n_start_call}">
          <converse-icon color="var(${color})" class="fa fa-phone" size="1em">Rec</converse-icon>
      </button>
      <div class="record-graph">
        <button class="stop-recording" title="${i18n_start_call}">
            <converse-icon color="var(${color})" class="fa fa-phone" size="1em">Stop</converse-icon>
        </button>
        <canvas class="visualizer"></canvas>
      </div>`;
};
