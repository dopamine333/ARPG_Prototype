from enum import Enum


GRAVITY=-2
class GameEvent(Enum):
    '''this is event type and this type is Enum'''
    press_down_space = 0
    start_Battle = 1
    end_Battle = 2
class InputEvent(Enum):
    key_down=6
    w=0
    a=1
    s=2
    d=3
    j=4
    k=5


class Layer(Enum):
    '''
    由上畫到下的
    environment->sprite->UI
    '''
    environment = 1
    sprite = 2
    UI = 3


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
class Face(Enum):
    up=0
    down=1
    right=2
    left=3
    front=4
    back=5