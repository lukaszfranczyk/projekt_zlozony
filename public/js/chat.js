'use strict';

var CHAT = CHAT || {
    connect: function(callbacks) {
        var ws = new WebSocket("ws://localhost:30000/connections");
        ws.onopen = function() {
            console.log("Connection has been opened");
        }
        ws.onmessage = function(evt) {
            console.log(evt);
            var data = JSON.parse(evt.data);
            try {
                callbacks[data.type](data);
            }
            catch(err) {
                console.log(err);
            }
        }
    },
    refreshUsers: function(data) {
        console.log("it's working :)");
        console.log(data);
    },
    recvMessage: function(data) {

    },
    sendMessage: function(data) {

    },
    run: function() {
        var onMessageEvents = {
            users_list: this.refreshUsers,
            message: this.recvMessage
        }
        this.connect(onMessageEvents);
    },
}