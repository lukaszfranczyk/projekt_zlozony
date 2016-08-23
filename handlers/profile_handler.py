import logging
from tornado.web import authenticated
from tornado.gen import coroutine
from .base_handler import BaseHandler


class ProfileHandler(BaseHandler):

    @authenticated
    @coroutine
    def get(self, *args, **kwargs):
        user_data = yield self.db.get_user(user_name=self.current_user)
        logging.info(user_data)
        self.render("profile.html", user_data=user_data)
