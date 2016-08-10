import momoko
from tornado import ioloop
from tornado.gen import coroutine
from utils import Collection


class PgApi(metaclass=Collection):

    __CONNECTION_POOL = 20

    def __init__(self, db_user, db_password, db_name, db_host, db_port):
        dsn = 'dbname={} user={} password={} host={} port={}'.format(
            db_name, db_user, db_password, db_host, db_port
        )
        self.db = momoko.Pool(dsn=dsn, size=self.__CONNECTION_POOL, ioloop=ioloop.IOLoop.instance())
        self.db.connect()
        print(dsn)

    @coroutine
    def check(self):
        cursor = yield self.db.execute('SELECT 1')
        print(cursor.fetchone())
