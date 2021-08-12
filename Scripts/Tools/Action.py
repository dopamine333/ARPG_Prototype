
class Action:
    def __init__(self) -> None:
        self.funcs = []

    def __add__(self, func):
        self.funcs.append(func)
        return self

    def __sub__(self, func):
        if func not in self.funcs:
            raise Exception("ActionError: Detach unkwon func.")
        self.funcs.remove(func)
        return self

    def __contains__(self, func):
        return func in self.funcs

    def notify(self, *args):
        for func in self.funcs:
            try :
                func(*args)
            except TypeError as e:
                raise Exception("ActionError: arguments num error , "+str(e))
            


# PEP 646
'''from typing import Callable, Generic

from typing_extensions import TypeVarTuple,Unpack
T = TypeVarTuple('T')
class Action(Generic[Unpack[T]]):
    def __init__(self) -> None:
        self.funcs:list[Callable[[Unpack[T]],None]]=[]
    def __iadd__(self,func:Callable[[Unpack[T]],None]):
        self.funcs.append(func)
        return self
    

    def __isub__(self,func:Callable[[Unpack[T]],None]):
        if func not in self.funcs:
            raise Exception("ActionError: Detach unkwon func.")
        self.funcs.remove(func)
        return self

    def __contains__(self, func:Callable[[Unpack[T]],None]):
        return func in self.funcs

    def notify(self,*args:Unpack[T]):
        for func in self.funcs:
            func(*args)'''
