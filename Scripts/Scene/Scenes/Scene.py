from __future__ import annotations
import pygame
from Scripts.Graph.Camera import Camera
import Scripts.Scene.SceneChanger
from Scripts.GameObject.GameObject import GameObject
class Scene:
    def __init__(self,scene_changer:Scripts.Scene.SceneChanger.SceneChanger) -> None:
        self.scene_changer=scene_changer
        self.gameobjects:list[GameObject]=[]
    def start(self):
        pass
    def end(self):
        pass
    def update(self):
        for gameobject in self.gameobjects:
            gameobject.update()
    def draw(self,camera:Camera):
        for gameobject in self.gameobjects:
            gameobject.draw(camera)
    def change_scene(self,new_scene_name:type[Scene]):
        self.scene_changer.change(new_scene_name(self.scene_changer))