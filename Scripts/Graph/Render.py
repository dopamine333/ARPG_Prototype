from __future__ import annotations
from Scripts.Graph.Camera import Camera
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


class Render:
    def __init__(self, screen: Surface) -> None:
        self.screen = screen
        self.camera:Camera=None
        transparent_surface = Surface(
            screen.get_size(), pygame.SRCALPHA).convert_alpha()
        self.layers: dict[Layer, Surface] = {
            Layer.UI: transparent_surface.copy(),
            Layer.sprite: transparent_surface.copy(),
        }
    def set_camera(self,camera:Camera):
        self.camera=camera

    def render(self):
        # clear screen
        if self.camera:
            self.camera.render(self.get_layer(Layer.sprite))
        self.screen.fill((150, 150, 150))
        for layer_name in Layer:
            layer=self.get_layer(layer_name)
            self.screen.blit(layer, (0, 0))
            layer.fill((0, 0, 0, 0))

    def draw(self, image: Image, position: Vector2,layer:Layer):
        self.get_layer(layer).blit(image.source, image.offset(position))
    
    def get_layer(self,layer:Layer):
        if not layer in self.layers:
            self.layers[layer]=Surface(self.screen.get_size(), pygame.SRCALPHA).convert_alpha()
        return self.layers[layer]