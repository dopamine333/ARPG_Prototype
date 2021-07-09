class Singleton(object):
    _instance=None

    @classmethod
    def Instance(cls):
        if not cls._instance:
            cls._instance=cls()
        return cls._instance