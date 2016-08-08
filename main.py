import tornado
import os
from tornado.web import Application, StaticFileHandler
from handlers import IndexHandler, LoginHandler


class MainHandler(Application):
    def __init__(self):
        root_dir = os.path.dirname(os.path.abspath(__file__))
        static_path = os.path.join(root_dir, 'public')
        settings = {
            "template_path": os.path.join(root_dir, 'templates'),
            "compiled_template_cache": False,
            "debug": True,
            "login_url": "/auth/login",
            "cookie_secret": "91d3c543bc00442a4cf5f674b0fb0fea",
            "xsrf_cookies": True
        }
        super().__init__(**settings)
        self.add_handlers("^.*$", [
            (r"/static/(.*)", StaticFileHandler, {"path": static_path}),
            (r"/", IndexHandler),
            (r"/auth/(login|signup)", LoginHandler)
        ])


if __name__ == '__main__':
    app = MainHandler()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()
