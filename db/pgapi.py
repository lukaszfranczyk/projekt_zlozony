import momoko
import psycopg2
import logging
from data_model import User
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

    @coroutine
    def create_user(self, name, password):
        try:
            insert_sql = 'INSERT INTO users (login, password) VALUES (%s, %s)'
            yield self.db.execute(insert_sql, [name, password])
            logging.info("User created")
        except Exception:
            logging.exception("There was problem to add user %s", name)
            return
        return 'OK'

    @coroutine
    def get_user(self, user_id=None, user_name=None):
        args = []
        if user_id is None and user_name is None:
            raise Exception("Invalid user_id and user_name")
        select_sql = 'SELECT id, login, password, first_name, last_name, email FROM users where '
        if user_id is not None:
            select_sql += 'id = %s'
            args.append(user_id)
        if user_name is not None:
            if user_id is not None:
                select_sql += ' AND '
            select_sql += 'login = %s'
            args.append(user_name)
        try:
            cursor = yield self.db.execute(select_sql, args, cursor_factory=psycopg2.extras.RealDictCursor)
        except Exception:
            logging.exception("There was a problem to get user %s", args)
            return

        if cursor.rowcount == 0:
            return

        temp = cursor.fetchone()

        return User(**temp)

