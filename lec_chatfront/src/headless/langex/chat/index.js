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
      return attrs
    }

    //Decode Corrected Messages
    api.listen.on('parseMessage',parseCorrectedMessage );

    api.listen.on('createMessageStanza', createCorrectedStanza);
  }
});