from Scripts.GameObject.Sprite.Character.Character import Character
from Scripts.Physics.Box import Box
from Scripts.Physics.FrozenRigidBody import FrozenRigidBody
from Scripts.CharacterBrain.SlimeBrain import SlimeBrain
from Scripts.Managers.PhysicsManager import PhysicsManager
from Scripts.GameObject.Sprite.Character.Slime import Slime
from Scripts.CharacterBrain.EnemyBrain import EnemyBrain
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
        PhysicsManager.Instance().set_activity_box(Box((640,360,640),(1280,720,1280)))
        
        hero_image = Image(
            load(r"Arts\Character\hero.png").convert_alpha(), (25, 123))
        hero_position = Vector3(720, 100, 720)
        hero_rigidbody = RigidBody(
            Collider(Vector3(25, 0, 25), Vector3(50, 123, 50)))
        player_controller = PlayerController()
        self.hero = Hero(hero_image, hero_position,
                         hero_rigidbody, player_controller)
        self.add_gameobjects(self.hero)

        slime_image = Image(
        load(r"Arts\Character\slime.png").convert_alpha(), (40, 40))
        for _ in range(5):
            slime_position = Vector3(
                random()*720, random()*200, random()*720)
            slime_rigidbody = RigidBody(
                Collider(Vector3(30, 0, 30), Vector3(60, 30, 60)))
            slime_brain = SlimeBrain()
            slime_brain.set_target(self.hero)
            slime = Slime(slime_image, slime_position,
                            slime_rigidbody, slime_brain)
            self.add_gameobjects(slime)

        obstacles = []
        for _ in range(8):
            size=random()*150+50
            obstacle_source = Surface((size, size),pygame.SRCALPHA).convert_alpha()
            obstacle_source.fill((random()*255, random()*200, random()*200))
            obstacle_image = Image(obstacle_source, Vector2(size/2,size))
            obstacle_position = Vector3(
                random()*1280, 0, random()*1280)
            obstacle_rigidbody = FrozenRigidBody(
                Collider(Vector3(size/2, 0, 10), Vector3(size, size, 20)))
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

        self.render:Render=None

    def release(self):
        self.to_mainmenu_button.detach(ButtonEvent.up, self.to_mainmenu)
        self.render.set_camera(None)
        self.render=None
    #TODO 想個比較好設定Camera的方式
    def draw(self, render: Render):
        if not self.render:
            self.render=render
        if not render.camera:
            render.set_camera(self.camera)        
        render.camera.update()
        super().draw(render)
    

    def to_mainmenu(self):
        self.change_scene(Scripts.Scene.Scenes.MainMenuScene.MainMenuScene)
