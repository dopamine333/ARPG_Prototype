from __future__ import annotations
from math import cos, sin
from time import time
from pygame import mouse
from pygame import transform
from pygame.draw import ellipse
from pygame.transform import rotate
from Scripts.Locals import Layer
from Scripts.Graph.Image import Image
import pygame
from pygame import Rect, Surface, Vector2, Vector3
from Scripts.Tools.BinaryTree import BinaryTree,Node


class Camera:
    def __init__(self) -> None:
        #TODO 相機跟隨玩家
        #self.position=Vector3()
        self.shadow_color = (20, 20, 30, 20)
        self.sprite_orders=BinaryTree(DrawSpriteOrder.get_comparison_value)
        self.world_to_screen_matrix:list[Vector2] = [
            Vector2(1, 0),  # x
            Vector2(0, -1),  # y
            Vector2(0, -0.5)  # z
        ]
        

 
    def update(self):
        mouse_pos=Vector2(mouse.get_pos())
        x=(mouse_pos.x/1280)-0.5
        y=mouse_pos.y/720
        self.world_to_screen_matrix[2].xy=Vector2(x,-y)

    def render(self,layer:Surface):
        sprite_layer=layer.copy()
        shadow_layer=layer.copy()
        #region draw sprites and shadow
        # 將sprite_orders根據z軸由遠排到近(大排到小)
        orders:list[DrawSpriteOrder]=self.sprite_orders.get_list()
        self.sprite_orders.clear()
        orders.reverse()
        for order in orders:
            # 在sprite_layer層上畫出sprite
            source = order.image.source
            position = self.world_to_screen(order.position,layer.get_height())
            topleft = order.image.offset(position)
            sprite_layer.blit(source, topleft)
            if order.shadow_size:
                shadow_position=order.position.xyz
                shadow_position.y=0
                # 在shadow_layer層上畫出橢圓形的shadow
                shadow_size_on_screen=\
                    order.shadow_size.x*self.world_to_screen_matrix[0]+\
                    Vector2(0,order.shadow_size.y*self.world_to_screen_matrix[2].y)
                shadow_size_on_screen.x=abs(shadow_size_on_screen.x)
                shadow_size_on_screen.y=abs(shadow_size_on_screen.y)
                shadow_rect = Rect(
                    (0, 0),
                    shadow_size_on_screen
                )
                shadow_rect.center = self.world_to_screen(shadow_position,layer.get_height())
                ellipse(shadow_layer, self.shadow_color, shadow_rect)

        layer.blit(shadow_layer,(0,0))
        layer.blit(sprite_layer,(0,0))


    def draw(self, image: Image, position: Vector3, shadow_size: Vector2=None):
        self.sprite_orders.insert(DrawSpriteOrder(image, position, shadow_size))

    def world_to_screen(self, world_position: Vector3,screen_height:float):
        """
        transform world position to screen position
        """
        screen_position = Vector2()
        screen_position += self.world_to_screen_matrix[0]*world_position.x
        screen_position += self.world_to_screen_matrix[1]*world_position.y
        screen_position += self.world_to_screen_matrix[2]*world_position.z
        screen_position.y += screen_height
        return screen_position
    

class DrawSpriteOrder:
    def __init__(self, image: Image, position: Vector3, shadow_size: Vector2) -> None:
        self.image = image
        self.position = position
        self.shadow_size = shadow_size
    @staticmethod
    def get_comparison_value(order:DrawSpriteOrder):
        return order.position.z
