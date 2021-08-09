from Scripts.Tools.Action import Action
from typing import Any, Callable


class EventManager:
    '''
    事件管理者

    可以註冊任何事件

    如果有人通知該事件則會廣播全部人
    '''
    events: dict[Any, Action] = {}

    @staticmethod
    def get(event: Any):
        if not event in EventManager.events:
            EventManager.events[event] = Action()
        return EventManager.events[event]
