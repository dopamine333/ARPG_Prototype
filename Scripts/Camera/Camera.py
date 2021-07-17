from __future__ import annotations
from Scripts.Graphic.RenderManager import RenderManager
from pygame import Color, mouse
from Scripts.GameObject.Component import Component
from pygame.draw import ellipse,rect
from Scripts.Graphic.Image import Image
import pygame
from pygame import Rect, Surface, Vector2, Vector3
from Scripts.Tools.BinaryTree import BinaryTree


class Camera(Component):
    '''
    將在世界座標的物件畫在Sprite圖層上

    並且有正確的遮擋排序和畫出影子
    '''

    def __init__(self) -> None:
        super().__init__()
        self.shadow_color = (20, 20, 40, 20)
        self.sprite_orders = BinaryTree(DrawSpriteOrder.get_comparison_value)
        self.world_to_screen_matrix: list[Vector2] = [
            Vector2(1, 0),  # x
            Vector2(0, -1),  # y
            Vector2(0, -0.5)  # z
        ]
        self.view_rect = Rect(0, 0, 0, 0)
        self.activity_rect: Rect = None


    def start(self):
        self.update_view_rect()

    def update_view_rect(self):
        self.view_rect.center = self.world_to_screen(
            self.position, self.view_rect.height)
        if self.activity_rect:
            self.view_rect.clamp_ip(self.activity_rect)


    def set_activity_rect(self, activity_rect: Rect):
        self.activity_rect = activity_rect
    def set_shadow_color(self, shadow_color: Color):
        self.shadow_color= shadow_color


    def update(self):
        #鏡頭轉動效果 測試用
        return
        mouse_pos=Vector2( mouse.get_pos())
        x=(mouse_pos.x/1280)-0.5
        y=mouse_pos.y/720
        self.world_to_screen_matrix[2].xy=Vector2(x,-y)

    def render(self, layer: Surface):
        '''將二元樹儲存的訂單畫在輸入的圖層上'''
        self.update_view_rect()

        sprite_layer = layer.copy()
        shadow_layer = layer.copy()

        # 將二元樹sprite_orders根據z軸由遠排到近(大排到小)
        orders: list[DrawSpriteOrder] = self.sprite_orders.get_list()
        self.sprite_orders.clear()
        orders.reverse()
        for order in orders:
            # 在sprite_layer層上畫出sprite
            source = order.image.source
            position = self.world_to_screen(order.position, layer.get_height())
            topleft = order.image.offset(position)-self.view_rect.topleft
            sprite_layer.blit(source, topleft)

            # 在shadow_layer層上畫出橢圓形的shadow
            if order.shadow_size:
                shadow_position = order.position.xyz
                shadow_position.y = 0
                shadow_size_on_screen =\
                    order.shadow_size.x*self.world_to_screen_matrix[0] +\
                    Vector2(0, order.shadow_size.y *
                            self.world_to_screen_matrix[2].y)
                shadow_size_on_screen.x = abs(shadow_size_on_screen.x)
                shadow_size_on_screen.y = abs(shadow_size_on_screen.y)
                shadow_rect = Rect(
                    (0, 0),
                    shadow_size_on_screen
                )
                shadow_rect.center = self.world_to_screen(
                    shadow_position, layer.get_height())
                shadow_rect.top -= self.view_rect.top
                shadow_rect.left -= self.view_rect.left
                ellipse(shadow_layer, self.shadow_color, shadow_rect)

        layer.blit(shadow_layer, (0, 0))
        layer.blit(sprite_layer, (0, 0))

    def draw(self, image: Image, position: Vector3, shadow_size: Vector2 = None):
        '''將參數打包成訂單，並插入二元樹sprite_orders中'''
        self.sprite_orders.insert(
            DrawSpriteOrder(image, position, shadow_size))

    def world_to_screen(self, world_position: Vector3, screen_height: float):
        '''
        將世界座標轉換成螢幕座標
        '''
        # 矩陣乘法再加上平移
        screen_position = Vector2()
        screen_position += self.world_to_screen_matrix[0]*world_position.x
        screen_position += self.world_to_screen_matrix[1]*world_position.y
        screen_position += self.world_to_screen_matrix[2]*world_position.z
        screen_position.y += screen_height
        return screen_position


class DrawSpriteOrder:
    '''儲存畫物件的參數'''

    def __init__(self, image: Image, position: Vector3, shadow_size: Vector2) -> None:
        self.image = image
        self.position = position
        self.shadow_size = shadow_size

    @staticmethod
    def get_comparison_value(order: DrawSpriteOrder):
        '''在二元樹sprite_orders中排序的值'''
        return order.position.z
