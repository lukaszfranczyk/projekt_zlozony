from tornado.gen import coroutine
from .base_handler import BaseHandler


class LoginHandler(BaseHandler):

    @coroutine
    def get(self, *args, **kwargs):
        self.render("login.html")

    @coroutine
    def post(self, *args, **kwargs):
        user_data = yield self.db.get_user(user_name=self.get_argument("login"))
        if user_data is None:
            yield self.db.create_user(self.get_argument("login"),
                                      self.get_argument("password"))
            self.redirect("/")
            return
        self.set_secure_cookie("user",  self.get_argument("login"), expires_days=1)
        self.redirect(self.get_argument("next", "/"))


class