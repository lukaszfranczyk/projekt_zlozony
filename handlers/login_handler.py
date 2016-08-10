from tornado.gen import coroutine
from .base_handler import BaseHandler


class LoginHandler(BaseHandler):

    @coroutine
    def get(self, *args, **kwargs):
        self.render("login.html")

    @coroutine
    def post(self, *args, **kwargs):
        self.set_secure_cookie("user",  self.get_argument("login"), expires_days=1)
        self.redirect(self.get_argument("next", "/"))