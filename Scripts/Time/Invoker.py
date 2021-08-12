from Scripts.Time.Time import Time
from typing import Callable


class Invoker:
    funcs: dict[Callable[[], None], float] = {}
    to_del_funcs: list[Callable[[], None]] = []

    @staticmethod
    def trigger():
        # invoke func
        for func in Invoker.to_del_funcs:
            del Invoker.funcs[func]
        Invoker.to_del_funcs.clear()

        for func in Invoker.funcs:
            Invoker.funcs[func] -= Time.get_deltatime()
            if Invoker.funcs[func] < 0:
                Invoker.to_del_funcs.append(func)
                func()

    @staticmethod
    def is_invoking(func: Callable[[], None]):
        return func not in Invoker.to_del_funcs and func in Invoker.funcs

    @staticmethod
    def invoke(func: Callable[[], None], timeleft: float):
        Invoker.funcs[func] = timeleft

    @staticmethod
    def cancel_invoke(func: Callable[[], None]):
        if not Invoker.is_invoking(func):
            raise Exception(f"InvokerError: {func} is not invoking")
        Invoker.to_del_funcs.append(func)
