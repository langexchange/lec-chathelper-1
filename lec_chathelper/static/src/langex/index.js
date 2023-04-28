converse.plugins.add('converse-debug', {

  dependencies: ['convese-chat', 'converse-chatboxes', 'converse-disco'],

  initialize () {
      const { _converse } = this;
      window._converse = _converse;


  }
});




converse.initialize({
      theme: 'langexchange',
      auto_away: 300,
      enable_smacks: true,
      loglevel: 'debug',
      omemo_default: false,
      prune_messages_above: 100,
      message_archiving: 'always',
      keepalive: true,
      // assets_path: '/chat/dist/',
      // muc_respect_autojoin: true,
      // muc_show_logs_before_join: true,
      // notify_all_room_messages: ['discuss@conference.conversejs.org'],
      view_mode: 'fullscreen',
      // websocket_url: 'ws://localhost:5280/xmpp-websocket',
      websocket_url: 'wss://localhost/chat/xmpp/ws',
      // websocket_url: 'wss://langexchange.giize.com/chat/ws',
      whitelisted_plugins: ['converse-debug', 'converse-langex-chat', 'langex-audio-toolkit', 'converse-correctview'],
      allow_non_roster_messaging: true,
      allow_message_corrections: false,
      render_media: true,

      // credentials_url: "http://localhost:8081/myapp/auth/credentials?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODc4NzIxMTYsImlhdCI6MTY3Nzg2NzMxNywidWlkIjoiN2U2ZDg2MDEtMDFhNy00NDAzLTllZWUtZmFjNzYwMWFhZTIwIn0.JVZeVxlXJ__X1JcEeVMOTyfmrPp11OFC5-_C8PzOx4A",
      // auto_login: false,
      // jid: "hello@localhost",
      // password: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODc4NzIxMTYsImlhdCI6MTY3Nzg2NzMxNywidW5hbWUiOiJoZWxsbyJ9.qsDnTnOBoESSpU9MwLm7wBcaWd_EF6GRzQvDqwDVX3o",
});




// import { _converse, api, converse } from "@converse/headless/core.js";

// async function onCorrectionFormSubmitted () {
//   //Get the correction html
//   const html = `I dont think <r>hello</r><b>guys<b></b>`

//   // const model = _converse._converse.chatboxes.get('vutl@localhost');
//   // // Send message with correct option
//   // await model.sendMessage({'body': html, spoiler_hint, 'is_corrected':true});
//   console.log(_converse)
// }

// Object.assign(converse, {onCorrectionFormSubmitted});
