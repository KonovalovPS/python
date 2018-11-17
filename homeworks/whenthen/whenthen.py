def whenthen(func):
    class Decorator:
        def __init__(self, func):
            self.func = func
            self.lst_when = []
            self.lst_then = []
        
        def when(self, func):
            if len(self.lst_when) == len(self.lst_then):
                self.lst_when.append(func)
            else:
                raise ValueError
            return self
                     
        def then(self, func):
            if len(self.lst_when) == len(self.lst_then) + 1:
                self.lst_then.append(func)
            else:
                raise ValueError
            return self
        
        def __call__(self, *args, **kwargs):
            if len(self.lst_when) == len(self.lst_then):
                for idx, item in enumerate(self.lst_when):
                    if item(*args, **kwargs):
                        return self.lst_then[idx](*args, **kwargs)
                    return self.func(*args, **kwargs)
            else:
                raise ValueError
        
    return Decorator(func)


@whenthen
def fact(x):
    return x * fact(x - 1)

@fact.when
def fact(x):
    return x == 0

@fact.then
def fact(x):
    return 1

print(fact(0))
print(fact(1))
print(fact(5))