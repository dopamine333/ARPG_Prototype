from enum import Enum, Flag, auto
from os import remove

from pygame import Vector3

'''
一些大家都可以存取的常量
把它當作取代字串(string)的東西就好

'''
GRAVITY = Vector3(0, -7000, 0)


class ForceMode(Enum):
    '''
    根據力種類不同選擇不同的力的模式(ForceMode)

    使在不同幀率(FPS)維持穩定的物理行為

    ForceMode.force   ->  施加一個持續的力時選擇

    ForceMode.impulse ->  施加一個瞬間的力時選擇
    '''
    force = 0
    impulse = 1


class GameEvent(Enum):
    add_gameobject = 0
    remove_gameobject = 1


class InputEvent(Enum):
    key_down = 6
    key_press = 7
    move_up = 0
    move_left = 1
    move_down = 2
    move_right = 3
    jump = 4
    fire = 5
    dash=9
    change_collision_type = 8


class Tag(Enum):
    default = auto()
    player = auto()
    enemy = auto()
class CharacterID(Enum):
    Hero=0
    Slime=1
    GoblinFighter=2
    GoblinShooter=3
    GoblinKing=4

class VisualEffectID(Enum):
    hero_move=auto()
    hero_jump=auto()
    hero_landing=auto()
    hero_attack=auto()
    hero_underattack=auto()
    hero_dead=auto()
    slime_move=auto()
    slime_jump=auto()
    slime_landing=auto()
    slime_attack=auto()
    slime_underattack=auto()
    slime_dead=auto()
    '''
    move=auto()
    jump=auto()
    landing=auto()
    attack=auto()
    underattack=auto()
    dead=auto()
    '''
    

class PlayMode(Enum):
    once = 0
    loop = 1
    pingpong = 2


class Layer(Enum):
    '''
    圖層種類(Enum)

    根據排序由上畫到下
    (environment->sprite->UI)
    '''
    environment = auto()
    sprite = auto()
    UI = auto()
    gizmo = auto


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


class Face(Flag):
    '''
    描述方向(Flag)
    '''
    up = 0b100000
    down = 0b010000
    right = 0b001000
    left = 0b000100
    front = 0b000010
    back = 0b000001
    around = right | left | front | back
    rightleft = right | left
    updown = up | down
    frontback = front | back
    all = right | left | front | back | up | down
