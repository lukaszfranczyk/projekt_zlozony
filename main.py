import tornado
import os
from tornado.web import Application, StaticFileHandler
from handlers import IndexHandler


class MainHandler(Application):

	def __init__(self):
		root_dir = os.path.dirname(os.path.abspath(__file__))
		static_path = os.path.join(root_dir, 'public')
		settings = {
			"template_path": os.path.join(root_dir, 'templates'),
			"compiled_template_cache": False,
			"debug": True
		}
		super().__init__(**settings)
		self.add_handlers("^.*$", [
			(r"/static/(.*)", StaticFileHandler, {"path": static_path}),
			(r"/", IndexHandler)
		])


if __name__ == '__main__':
	app = MainHandler()
	app.listen(8080)
	tornado.ioloop.IOLoop.current().start()
	
