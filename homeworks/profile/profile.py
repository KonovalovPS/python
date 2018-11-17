import datetime
from inspect import isfunction, isclass

def func_update(func, s=''):
    def new_func(*args, **kwargs):
        print('`{}{}` started'.format(s, func.__name__))
        time1 = datetime.datetime.now()
        a = func(*args, **kwargs)
        time2 = datetime.datetime.now()
        time_func = (time2 - time1).total_seconds()
        print('`{}{}` finished in {}s'.format(s, func.__name__, time_func))
        return a
    return new_func

def profile(obj):
    if isfunction(obj):
        return func_update(obj)
    if isclass(obj):
        klass = obj
        for attr_name in klass.__dict__:
            attr = getattr(klass, attr_name)
            if attr_name != '__dict__' and callable(attr):
                setattr(klass, attr_name, func_update(attr, s='{}_obj.'.format(klass.__name__)))
        return klass

@profile
def stupid_func():
    a = 1000000
    while a > 0:
        a -= 1
    print("I'm vegan")

@profile
class Myclass:
    def __init__(self, a):
        self.a = a

    def palma(self):
        print('I love palmas')
        
stupid_func()
a = Myclass(1)
a.palma()
