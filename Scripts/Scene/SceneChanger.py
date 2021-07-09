import pygame
from Scripts.Graph.Camera import Camera
import Scripts.Scene.Scenes.Scene


class SceneChanger:
    def __init__(self) -> None:
        self.current_scene = None

    def update(self):
        if self.current_scene:
            self.current_scene.update()

    def draw(self, camera: Camera):
        if self.current_scene:
            self.current_scene.draw(camera)

    def change(self, new_scene):
        print(f"change scene from {self.current_scene.__class__} to {new_scene.__class__}")
        if self.current_scene:
            self.current_scene.end()
        self.current_scene = new_scene
        self.current_scene.start()
