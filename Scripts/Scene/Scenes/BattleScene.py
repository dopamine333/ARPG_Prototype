from Scripts.GameSystem.GameManagerRunner import GameManagerRunner

from Scripts.Camera.CameraController import CameraController
from Scripts.Camera.Camera import Camera
from Scripts.Button.MouseManager import MouseManager
from Scripts.Button.Button import Button
from Scripts.GameObject.GameObject import GameObject
from Scripts.Graphic.Render.Render import Render

from Scripts.Graphic.Image import Image
from Scripts.Graphic.RenderManager import RenderManager
from Scripts.Physics.Physics import Physics
from Scripts.Physics.Box import Box
from Scripts.Physics.RigidBody import RigidBody
from Scripts.Locals import ButtonEvent, Layer
from pygame.image import load
import pygame
import Scripts.Scene.Scenes.MainMenuScene
from Scripts.Scene.Scenes.Scene import Scene
from pygame import Surface
from random import random
from Scripts.Graphic.Render.SpriteRender import SpriteRender


class BattleScene(Scene):
    def scene_start(self):
        # region obstacle
        for _ in range(8):
            size = random()*150+50
            obstacle_source = Surface(
                (size, size), pygame.SRCALPHA).convert_alpha()
            obstacle_source.fill((random()*255, random()*200, random()*200))
            obstacle = GameObject()
            obstacle_render = obstacle.add_component(SpriteRender)
            obstacle_rigidbody = obstacle.add_component(RigidBody)
            obstacle_rigidbody.set_frozen(True)
            obstacle_rigidbody.set_collider((size, size, 20), (size/2, 0, 10))
            obstacle_render.set_image(Image(obstacle_source, (size/2, size)))
            obstacle_render.set_shadow_size((size, 20))
            obstacle.set_position((random()*1280, 0, random()*1280))

            self.add_gameobject(obstacle)
        # endregion

        # region to_mainmenu_button

        to_mainmenu_button_source = load(
            r"Arts\BattleMenu\to_mainmenu.png").convert_alpha()
        to_mainmenu_button_size = to_mainmenu_button_source.get_size()
        to_mainmenu_button = GameObject()
        to_mainmenu_button_render = to_mainmenu_button.add_component(Render)
        to_mainmenu_button_button = to_mainmenu_button.add_component(Button)
        to_mainmenu_button_render.set_image(Image(to_mainmenu_button_source))
        to_mainmenu_button_render.set_layer(Layer.UI)
        to_mainmenu_button_button.set_button_size(to_mainmenu_button_size)
        to_mainmenu_button.set_position((1212, 665, 0))

        to_mainmenu_button_button.attach(ButtonEvent.up, self.to_mainmenu)
        self.add_gameobject(to_mainmenu_button)
        # endregion

        # region camera
        camera = GameObject()
        camera_camera = camera.add_component(Camera)
        camera_controller = camera.add_component(CameraController)
        camera_controller.set_follow_axis(y=False)
        camera.set_position((800, 500, 200))
        camera_controller.set_offset((0, 120, 0))
        camera_controller.set_follow_speed(0.4)
        camera_controller.set_max_follow_distance(15)
        # camera_controller.set_activity_rect(Rect(-500,-500,2000,2000))
        camera_camera.set_shadow_color((10, 10, 50, 50))
        self.add_gameobject(camera)
        # endregion

        RenderManager.set_camera(camera_camera)
        Physics.set_activity_box(Box((1280, 720, 1280), (640, 360, 640)))

        game_manager_runner = GameObject()
        game_manager_runner.add_component(GameManagerRunner)
        self.add_gameobject(game_manager_runner)

    def scene_update(self):
        MouseManager.update()
        Physics.update()

    def scene_end(self):
        RenderManager.set_camera(None)

    def to_mainmenu(self):
        self.change_scene(Scripts.Scene.Scenes.MainMenuScene.MainMenuScene)
