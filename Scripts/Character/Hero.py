from Scripts.Graphic.Render.SpriteRender import SpriteRender
from Scripts.Physics.Collision import Collision
from Scripts.Animation.Animator import Animator
from Scripts.Physics.Physics import Physics
from Scripts.Graphic.Image import Image
from Scripts.Graphic.RenderManager import RenderManager
from Scripts.Character.Character import Character
from random import random
import pygame
from Scripts.Attack.AttackParam import AttackParam
from Scripts.Locals import Face, Layer, Tag
from Scripts.Physics.Box import Box
from pygame.image import load
from Scripts.Physics.RigidBody import RigidBody
from pygame import Vector2, Vector3
import pygame.transform
# TODO 完成武器類別


class Hero(Character):
    def start(self):
        sword_flash_source = load(
            r"Arts\Character\sword_flash.png").convert_alpha()
        self.jump_force = 2500
        self.dash_force = 1000
        self.move_speed = 1728
        self.max_hp = 1000

        super().start()
        self.rigidbody.damp = 0.92

        self.sword_damage = 3
        self.sword_force = Vector3(1000, 1200, 0)
        self.sword_flash_image = Image(sword_flash_source, Vector2(45, 44))
        self.sword_flash_box_size = Vector3(100, 60, 100)
        self.sword_flash_offset = Vector3(100, 60, 0)

        self.animator = self.get_component(Animator)
        self.render= self.get_component(SpriteRender)

    def jump(self):
        super().jump()

    def update(self):
        super().update()
        self.animator.set_bool("on_ground", self.on_ground)
        if self.rigidbody.acceleration.length_squared()<1:
            self.animator.set_bool("running", False)
        else:
            self.animator.set_bool("running", True)
        self.render.set_face(self.face)
        #print(self.animator.current_animation.frame)
    
    def dead(self):
        self.animator.set_bool("dead",True)

    def attack(self):
        force = self.sword_force.xyz
        offset = self.sword_flash_offset.xyz
        image = Image(self.sword_flash_image.source,
                      self.sword_flash_image.center)
        if self.face == Face.left:
            force.x *= -1
            offset.x *= -1
            image.source = pygame.transform.flip(image.source, True, False)
        RenderManager.camera.draw(image, self.position+offset)
        box = Box(self.sword_flash_box_size, self.position+offset)
        rigidbodies = Physics.overlap_box(box)
        for rigidbody in rigidbodies:
            if rigidbody.compare_tag(Tag.enemy):
                target: Character = rigidbody.get_component(Character)
                attack_param = AttackParam(
                    round(self.sword_damage*random()+self.sword_damage/2), force)
                attack_param.set_attacker(self)
                target.under_attack(attack_param)
