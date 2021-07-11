from Scripts.Graph.Camera import Camera
from Scripts.Graph.Render import Render
from Scripts.GameObject.UI.Button import Button
from Scripts.Locals import ButtonEvent, Face
from Scripts.Physics.Collider import Collider
from Scripts.Physics.RigidBody import RigidBody
from pygame.image import load
from Scripts.Graph.Image import Image
from Scripts.GameObject.Sprite.Sprite import Sprite
from Scripts.GameObject.Sprite.Character.Hero import Hero
import pygame 
from time import time
import Scripts.Scene.Scenes.MainMenuScene
from Scripts.Scene.Scenes.Scene import Scene
from Scripts.Managers.EventManager import EventManager
from pygame import Surface, Vector2, Vector3
from Scripts.CharacterBrain.PlayerController import PlayerController
from random import random


class BattleScene(Scene):
    def init(self):
        self.start_time = time()

        self.camera=Camera()

        hero_image = Image(
            load(r"Arts\Character\hero.png").convert_alpha(), (25, 123))
        hero_position = Vector3(720, 100, 720)
        hero_rigidbody = RigidBody(
            Collider(Vector3(25, 0, 25), Vector3(50, 123, 50)))
        player_controller = PlayerController()
        self.hero = Hero(hero_image, hero_position,
                         hero_rigidbody, player_controller)
        self.add_gameobjects(self.hero)

        obstacles = []
        for _ in range(15):
            size=random()*150+50
            obstacle_source = Surface((size, size),pygame.SRCALPHA).convert_alpha()
            obstacle_source.fill((random()*255, random()*200, random()*200))
            obstacle_image = Image(obstacle_source, Vector2(size/2,size))
            obstacle_position = Vector3(
                random()*1280, random()*100, random()*1280)
            obstacle_rigidbody = RigidBody(
                Collider(Vector3(size/2, 0, size/4), Vector3(size, size, size/2)))
            obstacles.append(
                Sprite(obstacle_image, obstacle_position, obstacle_rigidbody))
        self.add_gameobjects(*obstacles)

        to_mainmenu_button_source = load(
            r"Arts\BattleMenu\to_mainmenu.png").convert_alpha()
        to_mainmenu_button_rect = to_mainmenu_button_source.get_rect()
        to_mainmenu_button_rect.center = (1212, 665)
        self.to_mainmenu_button = Button(Image(to_mainmenu_button_source),to_mainmenu_button_rect)
        self.to_mainmenu_button.attach(ButtonEvent.up,self.to_mainmenu)
        self.add_gameobjects(self.to_mainmenu_button)

    def release(self):
        self.to_mainmenu_button.detach(ButtonEvent.up, self.to_mainmenu)

    def draw(self, render: Render):
        if not render.camera:
            render.set_camera(self.camera)        
        self.camera.update()
        super().draw(render)
        

    def to_mainmenu(self):
        self.change_scene(Scripts.Scene.Scenes.MainMenuScene.MainMenuScene)
