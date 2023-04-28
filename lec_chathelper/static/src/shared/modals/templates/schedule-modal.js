import { __ } from 'i18n';
import { api } from "@converse/headless/core";
import { html } from 'lit';
import { modal_close_button } from "plugins/modal/templates/buttons.js";

export const tplFooter = (el) => {
  return html`
        <div class="modal-footer">
          <button class="btn btn-success">Submit</button>
          ${modal_close_button}
        </div>
    `;
}


export const tplScheduleModal = (el) => {

  return html`
        <div class="modal-body p-0 m-0 text-center">
          <label for="meeting-time">Choose a time for your appointment:</label>
          <input type="datetime-local"
            id="meeting-time"
            name="meeting-time"
            value="2018-06-12T19:30"
            min="2018-06-07T00:00"
            max="2018-06-14T00:00"
            style="border: solid 1px #ccc; border-radius: 4px; height: 32px; padding: 12px 12px; }"
          />
        </div>
    `;
}

