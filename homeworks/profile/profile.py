import datetime

def profile(obj):
    if str(type(obj)) == "<class 'function'>":
        def new_func(*args, **kwargs):
            func = obj
            print('`{}` started'.format(func.__name__))
            time1 = datetime.datetime.now()
            a = func(*args, **kwargs)
            time2 = datetime.datetime.now()
            time_func = (time2 - time1).total_seconds()
            print('`{}` finished in {}s'.format(func.__name__, time_func))
            return a
        return new_func


    if str(type(obj)) == "<class 'type'>":
        klass = obj
        for attr_name in klass.__dict__:
            attr = getattr(klass, attr_name)
            if attr_name != '__dict__':
                setattr(klass, attr_name, profile(attr))
        return klass


@profile
def stupid_func():
    a = 1000000
    while a > 0:
        a -= 1
    print("I'm vegan")

@profile
class A:
    def __init__(self, a):
        self.a = a

    def palma(self):
        print('I love palmas')

stupid_func()
a = A(1)
a.palma()