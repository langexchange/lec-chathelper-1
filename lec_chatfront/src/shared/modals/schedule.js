import BaseModal from "plugins/modal/modal.js";
import { tplScheduleModal, tplFooter } from "./templates/schedule-modal.js";
import { __ } from 'i18n';
import { api, converse } from "@converse/headless/core";

const u = converse.env.utils;


export default class ScheduleModal extends BaseModal {

  initialize() {
    super.initialize();
    this.listenTo(this.model, 'change', this.render);
    api.trigger('scheduleModalInitialized', this.model);
  }

  renderModal() {
    return tplScheduleModal(this);
  }

  renderModalFooter() {
    return tplFooter(this);
  }

  getModalTitle() {
    return 'Schedule chat'
  }

}

api.elements.define('converse-schedule-modal', ScheduleModal);
