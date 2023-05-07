
// window.addEventListener('converse-loaded', () => {
  converse.plugins.add('converse-debug', {
      initialize () {
          const { _converse } = this;
          window._converse = _converse;
      }
  });

  converse.initialize({
      theme: "langexchange",
      auto_away: 300,
      enable_smacks: true,
      loglevel: 'debug',
      omemo_default: false,
      prune_messages_above: 100,
      message_archiving: 'always',
      keepalive: true,
      assets_path: '/chat/dist/',
      // muc_respect_autojoin: true,
      // muc_show_logs_before_join: true,
      // notify_all_room_messages: ['discuss@conference.conversejs.org'],
      view_mode: 'fullscreen',
      websocket_url: 'wss://langexchange.giize.com/chat/ws',
      whitelisted_plugins: ['converse-debug'],
      allow_non_roster_messaging: true,
      // credentials_url: "http://localhost:8081/myapp/auth/credentials?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODc4NzIxMTYsImlhdCI6MTY3Nzg2NzMxNywidWlkIjoiN2U2ZDg2MDEtMDFhNy00NDAzLTllZWUtZmFjNzYwMWFhZTIwIn0.JVZeVxlXJ__X1JcEeVMOTyfmrPp11OFC5-_C8PzOx4A",
      // auto_login: false,
      // jid: "hello@localhost",
      // password: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImFiNjE2NTQ4LTA0NjAtNDAwOC1iYjI0LTlmZjdjZWY3YWQ5ZCIsInR5cCI6ImN1c3RvbWVyIiwiaW5jaWQiOiIzIiwibmJmIjoxNjc2ODY3MzE3LCJleHAiOjE2ODg0NzIxMTYsImlhdCI6MTY3Njg2NzMxNywidW5hbWUiOiJoZWxsbyJ9.vEJW4HupiW1ZrjXZU3Z-s_nyfgJCTWfJ2m8pi-iqBH0",
  });
// })

// window.addEventListener('converse-loaded', () => {
//   converse.plugins.add('converse-debug', {
//       initialize () {
//           const { _converse } = this;
//           window._converse = _converse;
//       }
//   });
//   converse.initialize({
//       reuse_scram_keys: true,
//       muc_subscribe_to_rai: true,
//       theme: 'dracula',
//       show_send_button: true,
//       auto_away: 300,
//       message_limit: 300,
//       // singleton: true,
//       // auto_join_rooms: ['ttt@conference.chat.example.org'],
//       auto_register_muc_nickname: true,
//       loglevel: 'debug',
//       // modtools_disable_assign: ['owner', 'moderator', 'participant', 'visitor'],
//       // modtools_disable_query: ['moderator', 'participant', 'visitor'],
//       enable_smacks: true,
//       // connection_options: { 'worker': '/dist/shared-connection-worker.js' },
//       // persistent_store: 'IndexedDB',
//       message_archiving: 'always',
//       // muc_domain: 'conference.chat.example.org',
//       muc_respect_autojoin: true,
//       view_mode: 'fullscreen',
//       // websocket_url: 'ws://chat.example.org:5380/xmpp-websocket',
//       websocket_url: 'ws://localhost:8080/xmpp-websocket',
//       // bosh_service_url: 'http://chat.example.org:5280/http-bind',
//       allow_user_defined_connection_url: true,
//       muc_show_logs_before_join: true,
//       whitelisted_plugins: ['converse-debug', 'converse-batched-probe'],
//       blacklisted_plugins: [],
//   });
// });
