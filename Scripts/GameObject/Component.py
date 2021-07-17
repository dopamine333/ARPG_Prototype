from __future__ import annotations

from pygame import Vector3
from Scripts.Locals import Tag
from Scripts.GameObject.GameObject import GameObject,ComponentType


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

    def add_component(self, component_type:ComponentType)->ComponentType:
        '''新增並回傳一個組件(Component)，並與此組件的遊戲物件綁定'''
        return self.gameobject.add_component(component_type)

    def get_component(self, component_type:ComponentType)->ComponentType:
        '''回傳一個在此組件的遊戲物件上其他組件(Component)，如果該組件的類別為輸入類別或輸入的子類'''
        return self.gameobject.get_component(component_type)

    def compare_tag(self, tag: Tag):
        '''回傳此組件的遊戲物件標籤(tag)是否為輸入'''
        return self.gameobject.compare_tag(tag)

    def start(self):
        pass

    def end(self):
        pass

    def update(self):
        pass

    def destroy(self):
        '''銷毀此組件的遊戲物件並從場景(Scene)上移除'''
        self.gameobject.destroy()
