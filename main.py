import tornado
import os
from tornado.web import Application, StaticFileHandler
from handlers import *
from utils.logger import Logger


class MainHandler(Application):

    def __init__(self):
        Logger()
        root_dir = os.path.dirname(os.path.abspath(__file__))
        static_path = os.path.join(root_dir, 'public')
        settings = {
            "template_path": os.path.join(root_dir, 'templates'),
            "compiled_template_cache": False,
            "debug": True,
            "login_url": "/auth/login",
            "cookie_secret": "91d3c543bc00442a4cf5f674b0fb0fea"
        }
        super().__init__(**settings)
        self.add_handlers("^.*$", [
            (r"/static/(.*)", StaticFileHandler, {"path": static_path}),
            (r"/", IndexHandler),
            (r"/auth/(login|signup)", LoginHandler),
            (r"/messages", MessagesViewHandler),
            (r"/connections", MessagesConnectionsHandler)
            (r"/profile/edit", ProfileHandler),
            (r"/profile/edit/(user|password)", ProfileHandler)
        ])


if __name__ == '__main__':
    app = MainHandler()
    app.listen(30000)
    tornado.ioloop.IOLoop.current().start()
