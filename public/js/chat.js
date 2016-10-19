'use strict';

var CHAT = CHAT || {
    activeUser: null,
    connect: function(callbacks) {
        var ws = new WebSocket("ws://localhost:30000/connections");
        ws.onopen = function() {
            console.log("Connection has been opened");
        }
        ws.onmessage = function(evt) {
            var data = JSON.parse(evt.data);
            try {
                callbacks[data.type](data);
            }
            catch(err) {
                console.log(err);
            }
        }
        return ws;
    },
    refreshUsers: function(data) {
        if($("#contacts-window").length > 0) {
            var $contacts = $("#contacts-window ul"),
                $active_user = $("#contacts-window ul li.active-user"),
                html = "";

            for(var i in data.data) {
                var name = data.data[i],
                    newMsgList = JSON.parse(localStorage.getItem("new-msg-list")),
                    classes = "";
                if(newMsgList && newMsgList.hasOwnProperty(name) && CHAT.activeUser != name) {
                    classes += "new-msg ";
                }
                if($active_user.length > 0 && $active_user.text() == name) {
                    classes += "active-user";
                }
                html += '<li class="' + classes + '" data-person=' + name + '>' + name + '</li>';
            }
            $contacts.html(html);
            $.each($contacts.children(), function() {
                var that = this;
                $(this).on('click', function(event) {
                    $contacts.find("li.active-user").removeClass("active-user");
                    $(this).addClass("active-user");
                    CHAT.activeUser = $(this).data('person');
                    $("#message-window").text("");
                    $("#text-window").show();
                    if($(this).hasClass("new-msg") && CHAT.activeUser == $(this).data("person")) {
                        $(this).removeClass("new-msg");
                        delete newMsgList[CHAT.activeUser];
                        localStorage.setItem("new-msg-list", JSON.stringify(newMsgList));
                    }
                   var userMessages = localStorage.getItem(CHAT.activeUser);
                   if(userMessages) {
                        userMessages = JSON.parse(userMessages);
                        var html = "";
                        for(var i in userMessages[CHAT.activeUser]) {
                            var msg = userMessages[CHAT.activeUser][i];
                            html += '<p class="';
                            switch(msg[0]) {
                                case "send":
                                    html += 'right-msg-board';
                                    break;
                                case "recv":
                                    html += 'left-msg-board';
                                    break;
                            }
                            html += '">' + msg[1] + '</p>';
                            $("#message-window").html(html);
                            CHAT.scrollToBottom();
                        }
                   }
                })
            });
        }
        else {
            CHAT.activeUser = null;
            $("#text-window").hide();
        }
    },
    scrollToBottom: function() {
        var $msg = $('#message-window');
        $msg.scrollTop($msg[0].scrollHeight);
    },
    saveHistory: function(message, person, type) {
        var history = localStorage.getItem(person);
        if(history != null) {
            history = JSON.parse(history);
        } else {
            history = {};
        }
        if(!history.hasOwnProperty(person)) {
            history[person] = [];
        }
        history[person].push([type, message]);
        localStorage.setItem(person, JSON.stringify(history));
    },
    recvMessage: function(data) {
        CHAT.saveHistory(data.data, data.recvFrom, 'recv');
        if(CHAT.activeUser == data.recvFrom) {
            $("#message-window").append('<p class="left-msg-board">' + data.data + '</p>');
            CHAT.scrollToBottom();
        }
        if(CHAT.activeUser != data.recvFrom) {
            var newMsgList = JSON.parse(localStorage.getItem('new-msg-list'));
            if(newMsgList == null) {
                newMsgList = {};
            }
            newMsgList[data.recvFrom] = new Date();
            localStorage.setItem('new-msg-list', JSON.stringify(newMsgList));
            $("#contacts-window ul li[data-person=" + data.recvFrom +"]").addClass("new-msg");
        }
    },
    sendMessage: function(sock) {
        function send() {
            var msg = $("#messages").val(),
                data = {
                    type: "message",
                    sendTo: CHAT.activeUser,
                    data: msg,
                };
            try {
                sock.send(JSON.stringify(data));
                CHAT.saveHistory(msg, CHAT.activeUser, 'send');
                $("#message-window").append('<p class="right-msg-board"">' + data.data + '</p>');
                CHAT.scrollToBottom();
            }
            catch(err) {
                console.warn(err);
            }
            $("#text-window textarea#messages").val("");
        }
        $("button#send-message").on('click', send);
        $("#text-window textarea#messages").on('keydown', function(ev) {
            if(ev.which == 13) { //enter
                if(!ev.shiftKey) {
                    ev.preventDefault();
                    send();
                }
            }
        })
    },
    run: function() {
        var onMessageEvents = {
            users_list: this.refreshUsers,
            message: this.recvMessage
        }
        this.sendMessage(this.connect(onMessageEvents));
    },
}