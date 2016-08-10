from hashlib import md5


class Singleton(type):

    _instance = None

    def __call__(cls, *args, **kwds):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__call__(*args, **kwds)
        return cls._instance


class Collection(type):

    _instances = {}

    def __call__(cls, **kwds):
        hash = md5(str(kwds).encode('utf-8')).hexdigest()
        if hash not in cls._instances:
            cls._instances[hash] = super(Collection, cls).__call__(**kwds)
        return cls._instances[hash]
