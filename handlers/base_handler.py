import logging
from tornado.web import RequestHandler
from utils import Config
from db.pgapi import PgApi


class BaseHandler(RequestHandler):

    @property
    def db(self):
        try:
            return PgApi(
                db_user=self.config['db_user'],
                db_password=self.config['db_password'],
                db_port=self.config['db_port'],
                db_name=self.config['db_name'],
                db_host=self.config['db_host']
            )
        except Exception:
            logging.exception("Could not connect to database")
            raise

    @property
    def config(self):
        try:
            return Config()
        except Exception:
            return {}

    def get_current_user(self):
        self.current_user = self.get_argument("user", None)
        if self.current_user is None:
            return
        try:
            if self.current_user != self.get_secure_cookie("user").decode('utf-8'):
                return
        except Exception:
            return
        return self.get_secure_cookie("user")
