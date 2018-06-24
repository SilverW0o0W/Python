import threading


class Singleton(object):
    _instance_lock = threading.Lock()

    def __init__(self, index):
        self.index = index

    def __new__(cls, *args, **kwargs):
        if not hasattr(Singleton, "_instance"):
            with Singleton._instance_lock:
                if not hasattr(Singleton, "_instance"):
                    Singleton._instance = object.__new__(cls)
        return Singleton._instance


if __name__ == '__main__':
    a = Singleton(1)
    b = Singleton(2)
    print(id(a))
    print(id(b))
