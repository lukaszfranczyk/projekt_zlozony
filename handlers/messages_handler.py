from tornado.web import authenticated
from tornado.gen import coroutine
from .base_handler import BaseHandler


class MessagesHandler(BaseHandler):

    @authenticated
    @coroutine
    def get(self, *args, **kwargs):
        self.render("messages.html")