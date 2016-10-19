from tornado.gen import coroutine
from .base_handler import BaseHandler


class LogoutHandler(BaseHandler):

    @coroutine
    def get(self, *args, **kwargs):
        self.clear_all_cookies()
        self.redirect("/")
