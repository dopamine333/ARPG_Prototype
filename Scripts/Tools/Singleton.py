class Singleton(object):
    '''繼承即成為單例模式'''
    _instance = None

    @classmethod
    def Instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance
