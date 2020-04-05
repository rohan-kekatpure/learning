def echo(func):
    def deco():
        print(func.__name__)
        func()
    return deco


@echo
def myfunc():
    print('inside myfunc')
