from Scripts.Camera.CameraController import CameraController
from Scripts.Button.MouseManager import MouseManager
from Scripts.Physics.Physics import Physics
from Scripts.Button.Button import Button
from Scripts.Graphic.Render.Render import Render
from Scripts.Character.Slime import Slime
from Scripts.Character.Hero import Hero
from Scripts.GameObject.GameObject import GameObject
from Scripts.Graphic.Image import Image
from Scripts.Camera.Camera import Camera
from Scripts.Graphic.RenderManager import RenderManager
from Scripts.Physics.Box import Box
from Scripts.Locals import ButtonEvent, Face, Layer, Tag
from Scripts.Physics.Collider import Collider
from Scripts.Physics.RigidBody import RigidBody
from pygame.image import load
import pygame
from time import time
import Scripts.Scene.Scenes.MainMenuScene
from Scripts.Scene.Scenes.Scene import Scene
from pygame import Rect, Surface
from random import random
from Scripts.Character.CharacterBrain.PlayerController import PlayerController
from Scripts.Character.CharacterBrain.SlimeBrain import SlimeBrain
from Scripts.Graphic.Render.SpriteRender import SpriteRender


class BattleScene(Scene):
    def scene_start(self):
        # region hero
        hero_image = Image(
            load(r"Arts\Character\hero.png").convert_alpha(), (25, 123))
        hero = GameObject()
        hero_hero = hero.add_component(Hero)
        hero_rigidbody = hero.add_component(RigidBody)
        hero_render = hero.add_component(SpriteRender)
        hero_rigidbody.set_collider(Collider((50, 123, 50), (25, 0, 25)))
        hero_hero.set_brain(PlayerController())
        hero_render.set_image(hero_image)
        hero_render.set_shadow_size((50, 50))
        hero.set_position((720, 100, 720))
        hero.set_tag(Tag.player)
        self.add_gameobject(hero)
        # endregion

        # region slime
        slime_image = Image(
            load(r"Arts\Character\slime.png").convert_alpha(), (40, 40))
        for _ in range(15):
            slime = GameObject()
            slime_rigidbody = slime.add_component(RigidBody)
            slime_slime = slime.add_component(Slime)
            slime_render = slime.add_component(SpriteRender)
            slime_render.set_image(slime_image)
            slime_render.set_shadow_size((60, 60))
            slime_rigidbody.set_collider(Collider((60, 30, 60), (30, 0, 30)))
            slime.set_position((random()*1280, random()*400, random()*1280))
            slime_brain = SlimeBrain()
            slime_brain.set_target(hero)
            slime_slime.set_brain(slime_brain)
            slime.set_tag(Tag.enemy)

            self.add_gameobject(slime)
        # endregion

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
            obstacle_rigidbody.set_collider(
                Collider((size, size, 20), (size/2, 0, 10)))
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

        #region camera
        camera=GameObject()
        camera_camera=camera.add_component(Camera)
        camera_controller=camera.add_component(CameraController)
        camera_controller.set_target(hero)
        camera_controller.set_follow_axis(y=False)
        camera_controller.set_offset((0,100,-100))
        camera_camera.set_activity_rect(Rect(-500,-500,2000,2000))
        camera_camera.set_shadow_color((10,10,50,50))
        self.add_gameobject(camera)
        #endregion



        RenderManager.set_camera(camera_camera)
        Physics.set_activity_box(Box((1280, 720, 1280), (640, 360, 640)))

    def scene_update(self):
        MouseManager.update()
        Physics.update()

    def scene_end(self):
        RenderManager.set_camera(None)

    def to_mainmenu(self):
        self.change_scene(Scripts.Scene.Scenes.MainMenuScene.MainMenuScene)
