from enum import Enum


class GameEvent(Enum):
    '''this is event type and this type is Enum'''
    press_down_space = 0
    start_Battle = 1
    end_Battle = 2


class InputEvent(Enum):
    pass


class Layer(Enum):
    UI = 0
    sprite = 1
    shadow = 2
    environment = 3


class ButtonEvent(Enum):
    down = 0
    enter = 1
    exit = 2
    over = 3
    up = 4
    drag = 5


class CursorState(Enum):
    normal = 0
    button = 1
