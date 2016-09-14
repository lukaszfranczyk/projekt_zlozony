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
        login, password = self.get_argument("login"), self.get_argument("password")
        if self.request.uri.startswith(self.SIGNUP):
            yield self.signup(login, password)
        elif self.request.uri.startswith(self.LOGIN):
            yield self.login(login, password)
        else:
            self.redirect("/")

    @coroutine
    def login(self, user, password):
        user_data = yield self.db.get_user(user_name=user)
        if user_data is None:
            self.render("login.html", error="Invalid username !")
            return
        if user_data.password == password:
            self.set_secure_cookie("user", user, expires_days=1)
            self.redirect("/?user={}".format(user))
        else:
            self.render("login.html", error="Invalid password !")

    @coroutine
    def signup(self, user, password):
        error = "User exists !"
        user_data = yield self.db.get_user(user_name=user)
        if user_data is None:
            ret = yield self.db.create_user(user, password)
            if ret == "OK":
                self.set_secure_cookie("user",  user, expires_days=1)
                self.redirect("/?user={}".format(user))
                return
            error = "Something went wrong, please try again later !"
        self.render("login.html", error=error)
