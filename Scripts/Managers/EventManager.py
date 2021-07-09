from typing import Callable
import enum

class Event(enum.Enum):
    '''this is event type and this type is Enum'''
    press_down_space=0
    start_Battle=1
    end_Battle=2
class EventManager:
    '''
    A manager of event,

    you can attach,detach,notify some func on some event
    '''
    events:dict[Event,list[Callable]]={}

    @staticmethod
    def attach(event: Event,func:Callable):
        '''
        Attach a func on a event.

        if someone notify this event,

        the func will be called.
        '''
        if not event in EventManager.events:
            EventManager.events[event]=[]
        EventManager.events[event].append(func)
    @staticmethod
    def detach(event: Event,func:Callable):
        '''
        Detach a func from the event.
        '''
        if not event in EventManager.events:
            raise Exception("detach the unkwon event!")
        if not func in EventManager.events[event]:
            raise Exception("detach the unkwon func!")

        EventManager.events[event].remove(func)
    @staticmethod
    def notify(event: Event,*args_of_func):
        '''
        Notify all func which is on the event.
        '''
        if not event in EventManager.events:
            return
        for func in EventManager.events[event]:
            print(func.__code__.co_varnames,func.__code__.co_argcount)
            if func.__code__.co_argcount==0 or func.__code__.co_varnames==('self',):
                func()
            else:
                func(args_of_func)
        