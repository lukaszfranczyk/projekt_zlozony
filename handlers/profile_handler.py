import logging
from tornado.web import authenticated
from tornado.gen import coroutine
from .base_handler import BaseHandler


class ProfileHandler(BaseHandler):

    EDIT = '/profile/edit'

    @authenticated
    @coroutine
    def get(self, *args, **kwargs):
        user_data = yield self.db.get_user(user_name=self.current_user)
        self.render("profile.html", user_data=user_data)

    @coroutine
    def post(self, *args, **kwargs):
        password = self.get_argument("password")
        first_name = self.get_argument("first_name")
        last_name = self.get_argument("last_name")
        email = self.get_argument("email")
        if self.request.uri.startswith(self.EDIT):
            yield self.edit(password, first_name, last_name, email)
        else:
            self.redirect("/")

    @coroutine
    def edit(self, password, first_name, last_name, email):
        user = self.get_current_user()
        if user is None or password is None:
            raise Exception("Error updating user: incomplete data")

        yield self.db.update_user(user, password, first_name, last_name, email)
