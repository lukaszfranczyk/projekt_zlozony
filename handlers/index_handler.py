from tornado.web import RequestHandler
from tornado.gen import coroutine


class IndexHandler(RequestHandler):

	@coroutine
	def get(self, *args, **kwargs):
		self.render("index.html")

