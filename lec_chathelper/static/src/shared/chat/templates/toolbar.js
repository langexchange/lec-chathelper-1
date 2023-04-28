import { __ } from 'i18n';
import { html } from 'lit';
import { until } from 'lit/directives/until.js';

function tplSendButton () {
    const i18n_send_message = __('Send the message');
    return html`<button type="submit" class="btn send-button" title="${ i18n_send_message }">
        <converse-icon color="var(--toolbar-btn-text-color)" class="fa fa-paper-plane" size="1em"></converse-icon>
    </button>`
}

export default (el) => {
  return html`
        <span class="toolbar-buttons toolbar-buttons-custom">${
    until(el.getButtons(), "")
  }</span>
        <!-- ${el.show_send_button ? tplSendButton() : ""} -->
    `;
};
