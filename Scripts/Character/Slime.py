
from Scripts.Animation.Animator import Animator
from enum import Flag
from Scripts.Locals import Face, ForceMode, Tag
from Scripts.Character.Character import Character
from Scripts.Physics.Collision import Collision
from Scripts.Attack.AttackParam import AttackParam
from random import random
from time import time
from Scripts.Physics.RigidBody import RigidBody
from pygame import Vector2, Vector3


class Slime(Character):
    def start(self):
        self.max_hp = 20
        self.jump_force = 1400
        self.move_speed = 1100
        self.jump_cd = 1.5*random()+0.8
        self.last_jump = 0

        self.collide_damage = 2

        super().start()
        self.rigidbody.damp = 0.93
        self.animator:Animator = self.get_component(Animator)

    def move(self, direction: Vector2):
        if self.jump_cd+self.last_jump < time() and self.on_ground:
            self.last_jump = time()

            self.on_ground = False
            direction.scale_to_length(self.move_speed)
            force = Vector3(direction.x, self.jump_force, direction.y)
            self.rigidbody.add_force(force, ForceMode.impulse)
            self.animator.set_trigger("jump")
            print(self.animator.current_animation.frame)

    def on_collide(self, collision: Collision):
        super().on_collide(collision)
        if not collision.gameobject:
            return
        if collision.gameobject.compare_tag(Tag.player):
            if collision.face in Face.around:
                target: Character = collision.gameobject.get_component(
                    Character)
                attack_param = AttackParam(
                    self.collide_damage)
                attack_param.set_attacker(self)
                target.under_attack(attack_param)
