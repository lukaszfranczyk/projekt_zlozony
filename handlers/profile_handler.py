import logging
from hashlib import md5
from tornado.web import authenticated
from tornado.gen import coroutine
from .base_handler import BaseHandler


class ProfileHandler(BaseHandler):

    EDIT_USER = '/profile/edit/user'
    EDIT_PASSWORD = '/profile/edit/password'

    @authenticated
    @coroutine
    def get(self, *args, **kwargs):
        user_data = yield self.db.get_user(user_name=self.current_user)
        self.render("profile.html", user_data=user_data)

    @authenticated
    @coroutine
    def post(self, *args, **kwargs):
        if self.request.uri.startswith(self.EDIT_USER):
            first_name = self.get_argument("first_name")
            last_name = self.get_argument("last_name")
            email = self.get_argument("email")
            yield self.edit_user(first_name, last_name, email)
        else:
            if self.request.uri.startswith(self.EDIT_PASSWORD):
                password = self.get_argument("password")
                yield self.edit_password(password)
            else:
                self.redirect("/")

    @authenticated
    @coroutine
    def edit_user(self, first_name, last_name, email):
        user = yield self.db.get_user(user_name=self.current_user)
        if user is None:
            raise Exception("Error updating user: incomplete data")

        yield self.db.update_user(user.id, first_name, last_name, email)

        self.redirect("/profile/edit?user=" + user.login)

    @authenticated
    @coroutine
    def edit_password(self, password):
        user = yield self.db.get_user(user_name=self.current_user)
        if user is None:
            raise Exception("Error updating user: incomplete data")

        yield self.db.update_password(user.id, password)

        self.redirect("/profile/edit?user=" + user.login)
