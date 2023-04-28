import { _converse, api, converse } from "@converse/headless/core"

// Commonly used utilities and variables can be found under the "env"
// namespace of the "converse" global.
const { Promise, Strophe, dayjs, sizzle, _, $build, $iq, $msg, $pres } = converse.env;

//  While it’s possible to add new methods to classes via the overrides feature, it’s better and more explicit to use composition with Object.assign.

// A better approach is to use the events and hooks emitted by Converse, and to add your code in event handlers. This is however not always possible, in which case the overrides are a powerful tool.

// Plugins often need their own additional configuration settings and you can add these settings with the _converse.api.settings.update method.

converse.plugins.add('converse-langex-chat', {
  dependencies: ['convese-chat', 'converse-chatboxes', 'converse-disco'],

  overrides: {
    //Encode Corrected Message
    // ChatBox: {
    //   async createMessageStanza(message) {
    //     const stanza = $msg({
    //       'from': _converse.connection.jid,
    //       'to': this.get('jid'),
    //       'type': this.get('message_type'),
    //       'id': message.get('edited') && u.getUniqueId() || message.get('msgid'),
    //     }).c('body').t(message.get('body')).up();

    //     //WHERE LANGEXCHANGE CHANGE
    //     if (message.get('is_corrected')) {
    //       console.log(stanza.cnode)
    //       stanza.cnode('<crr/>').up();
    //     }

    //     stanza.c(_converse.ACTIVE, { 'xmlns': Strophe.NS.CHATSTATES }).root();

    //     if (message.get('type') === 'chat') {
    //       stanza.c('request', { 'xmlns': Strophe.NS.RECEIPTS }).root();
    //     }

    //     if (!message.get('is_encrypted')) {
    //       if (message.get('is_spoiler')) {
    //         if (message.get('spoiler_hint')) {
    //           stanza.c('spoiler', { 'xmlns': Strophe.NS.SPOILER }, message.get('spoiler_hint')).root();
    //         } else {
    //           stanza.c('spoiler', { 'xmlns': Strophe.NS.SPOILER }).root();
    //         }
    //       }
    //       (message.get('references') || []).forEach(reference => {
    //         const attrs = {
    //           'xmlns': Strophe.NS.REFERENCE,
    //           'begin': reference.begin,
    //           'end': reference.end,
    //           'type': reference.type,
    //         }
    //         if (reference.uri) {
    //           attrs.uri = reference.uri;
    //         }
    //         stanza.c('reference', attrs).root();
    //       });

    //       if (message.get('oob_url')) {
    //         stanza.c('x', { 'xmlns': Strophe.NS.OUTOFBAND }).c('url').t(message.get('oob_url')).root();
    //       }
    //     }

    //     if (message.get('edited')) {
    //       stanza.c('replace', {
    //         'xmlns': Strophe.NS.MESSAGE_CORRECT,
    //         'id': message.get('msgid')
    //       }).root();
    //     }

    //     if (message.get('origin_id')) {
    //       stanza.c('origin-id', { 'xmlns': Strophe.NS.SID, 'id': message.get('origin_id') }).root();
    //     }
    //     stanza.root();

    //     /**
    //      * *Hook* which allows plugins to update an outgoing message stanza
    //      * @event _converse#createMessageStanza
    //      * @param { _converse.ChatBox | _converse.ChatRoom } - The chat from
    //      *      which this message stanza is being sent.
    //      * @param { Object } data - Message data
    //      * @param { _converse.Message | _converse.ChatRoomMessage } data.message
    //      *      The message object from which the stanza is created and which gets persisted to storage.
    //      * @param { Strophe.Builder } data.stanza
    //      *      The stanza that will be sent out, as a Strophe.Builder object.
    //      *      You can use the Strophe.Builder functions to extend the stanza.
    //      *      See http://strophe.im/strophejs/doc/1.4.3/files/strophe-umd-js.html#Strophe.Builder.Functions
    //      */
    //     const data = await api.hook('createMessageStanza', this, { message, stanza });
    //     return data.stanza;
    //   }
    // }
  },
  
  
 

  initialize() {
    function createCorrectedStanza(context, data){
      if(data.message.get('is_corrected')){
        data.stanza.c('crr').root();
        console.log(data.stanza.tree())
      }
      return data;
    }

    function parseCorrectedMessage(stanza, attrs){
      const is_corrected = stanza.querySelector('crr')? true: false;
      attrs = Object.assign(attrs, {is_corrected})
      console.log(attrs);
      return attrs
    }

    //Decode Corrected Messages
    api.listen.on('parseMessage',parseCorrectedMessage );

    api.listen.on('createMessageStanza', createCorrectedStanza);
  }
});