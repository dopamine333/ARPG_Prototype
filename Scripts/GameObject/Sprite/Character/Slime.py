
from Scripts.Physics.Collision import Collision
from Scripts.Attack.AttackParam import AttackParam
from random import random
from time import time
from Scripts.Physics.RigidBody import RigidBody
from Scripts.Graph.Image import Image
from Scripts.GameObject.Sprite.Character.Character import Character
from pygame import Vector2, Vector3


class Slime(Character):
    def start(self):
        super().start()
        self.force = 20
        self.jump_cd=1.5*random()+0.8
        self.last_jump=0
        self.rigidbody.set_damp(0.98)
        self.rigidbody.set_horizontal_max_speed(7)

        self.max_hp=20

    def move(self, direction: Vector2):
        if self.jump_cd+self.last_jump<time():
            self.last_jump=time()
            direction.normalize_ip()
            force=Vector3(direction.x,1,direction.y)*self.force
            self.rigidbody.add_force(force)
    #TODO 獲取玩家操作的角色
    def collide(self, collision: Collision):
        return
        if isinstance(collision.sprite,Character):
            pass
