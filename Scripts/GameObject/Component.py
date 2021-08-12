from __future__ import annotations
from typing import TYPE_CHECKING, Type
if TYPE_CHECKING:
    from Scripts.GameObject.GameObject import GameObject, ComponentType

from pygame import Vector3
from Scripts.Locals import Tag


class Component:
    '''
    場景上所有東西皆為遊戲物件(GameObject)和組件(Component)的結合

    若想新增一個功能則繼承此類

    屬性:
        +gameobject: GameObject
        +position: Vector3
    '''

    def __init__(self) -> None:
        self.gameobject: GameObject = None
        self.position: Vector3 = None

        '''self.enabled = True

    def set_enabled(self, value: bool):
        self.enabled = value

    def is_enabled(self):
        return self.enabled'''

    def add_component(self, component_type: Type[ComponentType]) -> ComponentType:
        '''新增並回傳一個組件(Component)，並與此組件的遊戲物件綁定'''
        return self.gameobject.add_component(component_type)

    def get_component(self, component_type: Type[ComponentType]) -> ComponentType:
        '''回傳一個在此組件的遊戲物件上其他組件(Component)，如果該組件的類別為輸入類別或輸入的子類'''
        return self.gameobject.get_component(component_type)

    def compare_tag(self, tag: Tag):
        '''回傳此組件的遊戲物件標籤(tag)是否為輸入'''
        return self.gameobject.compare_tag(tag)

    def awake(self):
        pass
    
    def start(self):
        pass

    def physics_update(self):
        pass

    def update(self):
        pass

    def animation_update(self):
        pass

    def late_update(self):
        pass

    def on_will_render_object(self):
        pass

    def on_destroy(self):
        pass

    def destroy(self):
        '''銷毀此組件的遊戲物件並從場景(Scene)上移除'''
        self.gameobject.destroy()
