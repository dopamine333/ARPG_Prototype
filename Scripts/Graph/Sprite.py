import pygame
from pygame import Surface, Vector3


class Sprite:
    def __init__(self, image: Surface, center: Vector3) -> None:
        self.image = image
        self.center = center
