import logging
from tornado.gen import coroutine
from .base_handler import BaseHandler


class LoginHandler(BaseHandler):

    SIGNUP = '/auth/signup'
    LOGIN = '/auth/login'

    @coroutine
    def get(self, *args, **kwargs):
        self.render("login.html", error="")

    @coroutine
    def post(self, *args, **kwargs):
        logging.info("IT'S WORKING")
        login, password = self.get_argument("login"), self.get_argument("password")
        if self.request.uri.startswith(self.SIGNUP):
            yield self.signup(login, password)
        elif self.request.uri.startswith(self.LOGIN):
            yield self.login(login, password)
        else:
            self.redirect("/")

    @coroutine
    def login(self, user, password):
        try:
            user_data = yield self.db.get_user(user_name=user)
        except Exception:
            self.redirect("/")
            return
        if user_data is None:
            self.render("login.html", error="Invalid username or password !")
            return
        error = "Invalid password"
        if user_data[1] == password:
            self.set_secure_cookie("user",  self.get_argument("login"), expires_days=1)
            error = ""
        self.redirect("/", error=error)

    @coroutine
    def signup(self, user, password):
        try:
            user_data = yield self.db.get_user(user_name=user)
        except Exception:
            self.redirect("/")
            return
        if user_data is None:
            yield self.db.create_user(user, password)
            self.set_secure_cookie("user",  password, expires_days=1)
            self.redirect("/")
            return
        self.render("login.html", error="User exists !")
