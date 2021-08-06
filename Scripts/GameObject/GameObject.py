from __future__ import annotations
from typing import TypeVar

from Scripts.GameObject.Component import Component
from typing import Type
from Scripts.Locals import Tag
from pygame import Vector3
from Scripts.Scene.SceneManager import SceneManager

ComponentType=TypeVar("ComponentType")
class GameObject:
    '''
    場景上所有東西皆為遊戲物件(GameObject)和組件(Component)的結合

    若想新增一個物件則創建此類

    屬性:
        +tag: Tag = Tag.default
        +position: Vector3 = Vector3(0,0,0)
    '''

    def __init__(self) -> None:
        self.components = []
        self.tag = Tag.default
        self.position = Vector3()

    # region setter

    def set_position(self, position: Vector3):
        self.position.xyz = position

    def set_tag(self, tag: Tag):
        self.tag = tag

    # endregion

    def start(self):
        '''當場景(Scene)開始或此遊戲物件加入場景(instantiate)時呼叫'''
        for component in self.components:
            component.start()

    def end(self):
        '''當場景(Scene)結束或此遊戲物件銷毀(destroy)時呼叫'''
        for component in self.components:
            component.end()

    def update(self):
        for component in self.components:
            component.update()

    def add_component(self, component_type:Type[ComponentType])-> ComponentType:
        '''新增並回傳一個組件(Component)，並與此遊戲物件綁定'''
        component = component_type()
        component.gameobject = self
        component.position = self.position
        self.components.append(component)
        return component

    def get_component(self, component_type:Type[ComponentType])->ComponentType:
        '''回傳一個組件(Component)，如果該組件的類別為輸入類別或輸入的子類'''
        for component in self.components:
            if isinstance(component, component_type):
                return component
        return None

    def compare_tag(self, tag: Tag):
        '''回傳此遊戲物件的標籤(tag)是否為輸入'''
        return self.tag == tag

    def destroy(self):
        '''銷毀此遊戲物件並從場景(Scene)上移除'''
        SceneManager.current_scene.destroy_gameobject(self)

    def instantiate(self):
        '''新增此遊戲物件到場景(Scene)上'''
        SceneManager.current_scene.instantiate_gameobject(self)
