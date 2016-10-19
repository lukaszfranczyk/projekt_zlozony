from tornado.web import authenticated
from tornado.gen import coroutine
from .base_handler import BaseHandler


class IndexHandler(BaseHandler):

    @authenticated
    @coroutine
    def get(self, *args, **kwargs):
        board_messages = yield self.db.get_board_messages()
        self.render("index.html", current_user=self.current_user, board_messages=board_messages)
