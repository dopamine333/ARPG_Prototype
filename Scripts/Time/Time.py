from time import time
from typing import Callable
from pygame.time import Clock


class Time:
    clock = Clock()
    target_fps = 60
    current_fps = 60
    deltatime = 1/60
    lasttime = time()
    paused = False

    invoke_funcs: dict[Callable[[], None], float] = {}
    to_del_invoke_funcs: list[Callable[[], None]] = []

    @staticmethod
    def is_paused():
        return Time.paused

    @staticmethod
    def pause():
        Time.paused = True

    @staticmethod
    def resume():
        Time.paused = False

    @staticmethod
    def get_deltatime():
        return Time.deltatime

    @staticmethod
    def set_target_fps(value):
        Time.target_fps = value

    @staticmethod
    def get_current_fps():
        return Time.current_fps

    @staticmethod
    def tick():
        Time.clock.tick(Time.target_fps)
        if not Time.paused:
            Time.deltatime = time() - Time.lasttime
            Time.lasttime = time()
            Time.current_fps = 1/Time.deltatime
        else:
            Time.deltatime = 0
            Time.lasttime = time()
            Time.current_fps = 0

        # invoke func
        for func in Time.to_del_invoke_funcs:
            del Time.invoke_funcs[func]
        Time.to_del_invoke_funcs.clear()

        to_call = []
        for func in Time.invoke_funcs:
            Time.invoke_funcs[func] -= Time.deltatime
            if Time.invoke_funcs[func] < 0:
                Time.to_del_invoke_funcs.append(func)
                to_call.append(func)

        for func in to_call:
            func()

    @staticmethod
    def invoke(func: Callable[[], None], timeleft: float):
        Time.invoke_funcs[func] = timeleft

    @staticmethod
    def cancel_invoke(func: Callable[[], None]):
        if not func in Time.invoke_funcs or func in Time.to_del_invoke_funcs:
            return
        Time.to_del_invoke_funcs.append(func)
