from typing import Any, Callable


class EventManager:
    '''
    事件管理者

    可以註冊任何事件

    如果有人通知該事件則會廣播全部人
    '''
    events: dict[Any, list[Callable]] = {}

    @staticmethod
    def attach(event: Any, func: Callable):
        '''
        註冊一個事件

        如果有人通知該事件則會廣播全部人
        '''
        if not event in EventManager.events:
            EventManager.events[event] = []
        EventManager.events[event].append(func)

    @staticmethod
    def detach(event: Any, func: Callable):
        '''
        取消註冊一個事件
        '''
        if not event in EventManager.events:
            raise Exception("detach the unkwon event!")
        if not func in EventManager.events[event]:
            raise Exception("detach the unkwon func!")

        EventManager.events[event].remove(func)

    @staticmethod
    def notify(event: Any, *args_of_func):
        '''
        通知所有註冊此事件的人
        '''
        if not event in EventManager.events:
            return
        for func in EventManager.events[event]:
            if func.__code__.co_argcount == 0 or func.__code__.co_varnames == ('self',):
                func()
            else:
                func(*args_of_func)
