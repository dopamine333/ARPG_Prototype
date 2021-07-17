from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Scripts.Camera.Camera import Camera
from pygame.time import Clock
from Scripts.Locals import Layer
from Scripts.Graphic.Image import Image
import pygame
from pygame import Surface, Vector2, Vector3


class RenderManager:
    '''
    提供物件畫在螢幕上的功能

    並根據圖層依序堆疊
    '''
    screen: Surface = None
    camera: Camera = None
    layers: dict[Layer, Surface] = {}

    @staticmethod
    def set_screen(screen: Surface):
        RenderManager.screen = screen

    @staticmethod
    def set_camera(camera: Camera):
        RenderManager.camera = camera
        if camera:
            camera.view_rect.size = RenderManager.screen.get_size()

    @staticmethod
    def render():
        '''將所有圖層堆疊並畫在螢幕上'''
        # 清空螢幕
        RenderManager.screen.fill((150, 150, 150))
        # 要求camera將世界座標物件的畫在Layer.sprite上
        if RenderManager.camera:
            RenderManager.camera.render(RenderManager.get_layer(Layer.sprite))
        # 將塗層依序畫到螢幕後清空該圖層
        for layer_name in Layer:
            layer = RenderManager.get_layer(layer_name)
            RenderManager.screen.blit(layer, (0, 0))
            layer.fill((0, 0, 0, 0))

    @staticmethod
    def draw(image: Image, position: Vector2, layer: Layer):
        '''輸入圖片、位置、圖層，將圖片畫在該圖層上'''
        RenderManager.get_layer(layer).blit(
            image.source, image.offset(position))

    @staticmethod
    def get_layer(layer: Layer):
        '''取得圖層，如果沒有該圖層就生成一個'''
        if not layer in RenderManager.layers:
            RenderManager.layers[layer] = Surface(
                RenderManager.screen.get_size(), pygame.SRCALPHA).convert_alpha()
        return RenderManager.layers[layer]
