from __future__ import annotations
from typing import TypeVar, Type
from Scripts.Locals import Tag
from pygame import Vector3
from Scripts.Scene.SceneManager import SceneManager

from Scripts.GameObject.Component import Component
ComponentType = TypeVar("ComponentType", bound=Component)


class GameObject:
    '''
    場景上所有東西皆為遊戲物件(GameObject)和組件(Component)的結合

    若想新增一個物件則創建此類

    屬性:
        +tag: Tag = Tag.default
        +position: Vector3 = Vector3(0,0,0)
    '''

    def __init__(self) -> None:
        self.components: list[Component] = []
        self.tag = Tag.default
        self.position = Vector3()
        '''self.enabled = True

    def set_enabled(self, value: bool):
        self.enabled = value

    def is_enabled(self):
        return self.enabled'''
    # region setter

    def set_position(self, position: Vector3):
        self.position.xyz = position

    def set_tag(self, tag: Tag):
        self.tag = tag

    # endregion

    def awake(self):
        for component in self.components:
            component.awake()

    def start(self):
        '''當場景(Scene)開始或此遊戲物件加入場景(instantiate)時呼叫'''
        for component in self.components:
            component.start()

    def physics_update(self):
        for component in self.components:
            component.physics_update()

    def update(self):
        '''if not self.is_enabled():
            return'''
        for component in self.components:
            '''if component.is_enabled():'''
            component.update()

    def animation_update(self):
        for component in self.components:
            component.animation_update()

    def late_update(self):
        for component in self.components:
            component.late_update()

    def on_will_render_object(self):
        for component in self.components:
            component.on_will_render_object()

    def on_destroy(self):
        for component in self.components:
            component.on_destroy()

    def add_component(self, component_type: Type[ComponentType]) -> ComponentType:
        '''新增並回傳一個組件(Component)，並與此遊戲物件綁定'''
        component = component_type()
        component.gameobject = self
        component.position = self.position
        self.components.append(component)
        return component

    def get_component(self, component_type: Type[ComponentType]) -> ComponentType:
        '''回傳一個組件(Component)，如果該組件的類別為輸入類別或輸入的子類'''
        for component in self.components:
            if isinstance(component, component_type):
                return component
        return None

    def compare_tag(self, tag: Tag):
        '''回傳此遊戲物件的標籤(tag)是否為輸入'''
        return self.tag in tag

    def destroy(self):
        '''銷毀此遊戲物件並從場景(Scene)上移除'''
        SceneManager.current_scene.destroy(self)

    def instantiate(self):
        '''新增此遊戲物件到場景(Scene)上'''
        SceneManager.current_scene.instantiate(self)

    '''def dont_destroy_on_load(self):
        SceneManager.dont_destroy_on_load(self)'''
