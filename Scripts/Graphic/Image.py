import pygame
from pygame import Surface, Vector3
from pygame.math import Vector2


class Image:
    """
    儲存圖像(Surface)的基於的中心座標
    """

    def __init__(self, source: Surface, center: Vector2 = None) -> None:
        '''中心座標(center)預設為圖片(source)的中間'''
        self.source = source
        if not center:
            center = Vector2(source.get_rect().center)
        self.center = Vector2(center)

    def offset(self, position: Vector2) -> Vector2:
        """
        回傳圖片(Surface)偏移後的左上角座標
        """
        return position-self.center

    def get_int_center(self) -> tuple[int, int]:
        """
        將中心座標轉型成整數數組(tuple[int,int])
        """
        return (round(self.center.x), round(self.center.y))
