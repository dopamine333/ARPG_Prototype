import pygame
from pygame import Surface, Vector3
from pygame.math import Vector2


class Image:
    def __init__(self, source: Surface, center: Vector2 = None) -> None:
        self.source = source
        if not center:
            center = source.get_rect().center
        self.center = Vector2(center)

    def offset(self, position: Vector2) -> Vector2:
        """
        return the topleft 

        when the center of image on the position
        """
        return position-self.center

    def get_int_center(self):
        return (round(self.center.x), round(self.center.y))
