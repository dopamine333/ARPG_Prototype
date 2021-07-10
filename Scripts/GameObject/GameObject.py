
from Scripts.Graph.Camera import Camera
from Scripts.Graph.Image import Image
import pygame
from pygame import Vector3


class GameObject:
    def __init__(self) -> None:
        self.image: Image = None

    def start(self):
        pass

    def end(self):
        pass

    def update(self):
        pass

    def draw(self, camera: Camera):
        pass
