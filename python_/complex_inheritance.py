class Foo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self._bar = None

    @property
    def bar(self):
        if self._bar is not None:
            return self._bar

        self._bar = Bar(self.x)
        return self._bar
            

class Bar(Foo):
    def __init__(self, x):
        super().__init__(x, 0)

    @property
    def bar(self):
        raise NotImplementedError('Property `bar` not available in class `Bar`')
        

if __name__ == '__main__':
    foo = Foo(1, 2)
    print(f'foo.x = {foo.x}, foo.y = {foo.y}')
    print(f'foo.bar.x = {foo.bar.x}, foo.bar.y = {foo.bar.y}')
    print(foo.bar.bar.x)
    