
from random import random
from pygame import image
import pygame
from Scripts.Graph.Render import Render
from Scripts.Attack.AttackParam import AttackParam
from Scripts.Locals import Face, Layer
from Scripts.Physics.Box import Box
from pygame.image import load
from Scripts.Managers.PhysicsManager import PhysicsManager
from Scripts.Physics.RigidBody import RigidBody
from Scripts.Graph.Image import Image
from Scripts.GameObject.Sprite.Character.Character import Character
from pygame import Vector2, Vector3
import pygame.transform
#TODO 完成武器類別
class Hero(Character):
    def start(self):
        sword_flash_source=load(r"Arts\Character\sword_flash.png").convert_alpha()
        super().start()
        self.force = 35
        self.speed = 2
        self.rigidbody.set_damp(0.92)
        self.rigidbody.set_horizontal_max_speed(6)
        
        self.sword_damage=3
        self.sword_force=Vector3(70,20,0)
        self.sword_flash_image=Image(sword_flash_source,Vector2(45,44))
        self.sword_flash_box_size=Vector3(100,60,100)
        self.sword_flash_offset=Vector3(100,60,0)
        self.draw_sword_flash=False

    def attack(self):
        self.draw_sword_flash=True
        force=self.sword_force.xyz
        offset=self.sword_flash_offset.xyz
        if self.face==Face.left:
            force.x*=-1
            offset.x*=-1
        box=Box(self.position+offset,self.sword_flash_box_size)
        rigidbodies=PhysicsManager.Instance().overlap_box(box)
        for rigidbody in rigidbodies:
            if isinstance(rigidbody.sprite,Character):
                target:Character=rigidbody.sprite
                attack_param= AttackParam(round(self.sword_damage*random()+self.sword_damage/2),force)
                attack_param.set_attacker(self)
                target.under_attack(attack_param)
    def draw(self, render: Render):
        if self.draw_sword_flash:
            offset=self.sword_flash_offset.xyz
            image=Image(self.sword_flash_image.source,self.sword_flash_image.center)
            if self.face==Face.left:
                offset.x*=-1
                image.source=pygame.transform.flip(image.source,True,False)
            render.camera.draw(image,self.position+offset)
            self.draw_sword_flash=False
        return super().draw(render)