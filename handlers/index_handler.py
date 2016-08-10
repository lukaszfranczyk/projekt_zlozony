from tornado.web import authenticated
from tornado.gen import coroutine
from .base_handler import BaseHandler


class IndexHandler(BaseHandler):

    @authenticated
    @coroutine
    def get(self, *args, **kwargs):
        yield self.db.check()
        self.render("index.html")
