import logging
import json
from tornado.ioloop import PeriodicCallback, IOLoop
from tornado.web import authenticated
from tornado.websocket import WebSocketHandler
from tornado.gen import coroutine
from .base_handler import BaseHandler


class MessagesViewHandler(BaseHandler):

    @authenticated
    @coroutine
    def get(self, *args, **kwargs):
        self.render("messages.html")


class MessagesConnectionsHandler(WebSocketHandler):

    __active_users = {}
    __conn_options = {"refresh": False}
    __max_list_buffer_size = 20
    __messages = {}

    def __init__(self, *args, **kwargs):
        super(MessagesConnectionsHandler, self).__init__(*args, **kwargs)
        if not self.__conn_options['refresh']:
            try:
                schedule = PeriodicCallback(MessagesConnectionsHandler.update_clients_list, 5000, IOLoop.instance())
                schedule.start()
            except Exception:
                logging.exception("Could not start active_user scheduler")
            else:
                self.__conn_options['refresh'] = True

    @classmethod
    def update_clients_list(cls):
        for instance in cls.__active_users.values():
            data = {
                "type": "users_list",
                "sendTo": "all",
                "recvFrom": "server",
                "data": list(cls.__active_users.keys())
            }
            instance.write_message(json.dumps(data))

    def open(self):
        self.__active_users[self.get_secure_cookie('user').decode('utf-8')] = self

    def on_message(self, data):
        data = json.loads(data)
        if data["type"] == "message":
            data["recvFrom"] = self.get_secure_cookie('user').decode('utf-8')
            user = data["sendTo"]
            if user in self.__active_users:
                self.__messages.setdefault(data["recvFrom"], [1]).append(data)
                self.__messages.setdefault(data["sendTo"], [1]).append(data)
                if len(self.__messages.setdefault(data["recvFrom"])) >= self.__max_list_buffer_size:
                    self.__messages[data["recvFrom"]] = []
                if len(self.__messages.setdefault(data["sendTo"])) >= self.__max_list_buffer_size:
                    self.__messages[data["sendTo"]] = []
                self.__active_users[user].write_message(json.dumps(data))


    def on_close(self):
        try:
            del self.__active_users[self.get_secure_cookie('user').decode('utf-8')]
        except Exception:
            logging.warn("Connection not exists anymore")
