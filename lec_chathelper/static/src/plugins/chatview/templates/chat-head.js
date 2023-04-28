import { __ } from 'i18n';
import { _converse } from '@converse/headless/core';
import { getStandaloneButtons, getDropdownButtons } from 'shared/chat/utils.js';
import { html } from "lit";
import { until } from 'lit/directives/until.js';

export default (o) => {
    const i18n_profile = __("The User's Profile Image");
    const avatar = html`<span title="${i18n_profile}">
        <converse-avatar
            class="avatar chat-msg__avatar"
            .data=${o.model.vcard?.attributes}
            nonce=${o.model.vcard?.get('vcard_updated')}
            height="40" width="40"></converse-avatar></span>`;
    const display_name = o.model.getDisplayName();

    return html`
        <div class="chatbox-title ${o.status ? '' : "chatbox-title--no-desc"}">
            <div class="chatbox-title--row">
                ${(!_converse.api.settings.get("singleton")) ? html`<converse-controlbox-navback jid="${o.jid}"></converse-controlbox-navback>` : ''}
                ${(o.type !== _converse.HEADLINES_TYPE) ? html`<a class="show-msg-author-modal" @click=${o.showUserDetailsModal}>${avatar}</a>` : ''}
                <div class="chatbox-title__text" title="${o.jid}">
                    ${(o.type !== _converse.HEADLINES_TYPE) ? html`<a class="user show-msg-author-modal" @click=${o.showUserDetailsModal}>${display_name}</a>` : display_name}
                </div>
            </div>
            <div class="chatbox-title__buttons row no-gutters">
                ${until(getDropdownButtons(o.heading_buttons_promise), '')}
                ${until(getStandaloneButtons(o.heading_buttons_promise), '')}
            </div>
        </div>
        ${o.status ? html`<p class="chat-head__desc">${o.status}</p>` : ''}
        <div class="schedule-container d-flex align-items-center w-100 justify-content-between px-3 py-2">
            <div class="d-flex align-items-center">
                <converse-icon size="28px" class="fa fa-calendar"></converse-icon>
                <div class="content text-dark font-weight-normal ml-2">
                    <strong class="text-dark">Nguyen Van A</strong> đã đặt lịch hẹn với bạn vào <strong class="text-info">Thứ 2, 12/10/2020</strong> lúc <strong class="text-info">10:00</strong>
                </div>
            </div>
            <div class="actions">
                <button class="btn btn-success btn-sm">Đồng ý</button>
                <button class="btn btn-secondary btn-sm">Lần tới</button>
            </div>
        </div>
    `;
}
