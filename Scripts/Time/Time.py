from time import time
from pygame.time import Clock


class Time:
    clock = Clock()
    target_fps = 60
    current_fps = 60
    deltatime = 1/60
    lasttime = time()
    paused = False

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
