from functools import wraps


def retry(func):
    @wraps(func)
    def ret_fn(self, *args, **kws):
        val = func(self, *args, **kws)
        if val == 0:
            self.attr = 10
            val = func(self, *args, **kws)
        return val
    return ret_fn


class Foo:
    def __init__(self, attr):
        self.attr = attr

    @retry
    def get(self):
        return self.attr


if __name__ == '__main__':
    foo = Foo(0)
    print(foo.get())


