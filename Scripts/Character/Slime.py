
from Scripts.Tools.Buffer import Buffer
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
        self.invincible_time=0
        super().start()

        self.jump_force = 2800
        self.move_speed = 1100
        self.rigidbody.damp = 0.93

        self.jumpbuffer = Buffer()
        self.can_jump_since_exit_ground_time = 0.05
        self.can_jump_before_enter_ground_time = 0.05

        self.move_cd = 2.5+0.8*random()
        self.jump_cd = 0.5

        self.collide_damage = 2

        self.animator: Animator = self.get_component(Animator)

    def jump(self):
        self.jumpbuffer.set("jump", self.can_jump_before_enter_ground_time)

    def do_jump(self):
        self.rigidbody.add_force((0, self.jump_force, 0), ForceMode.impulse)
        self.jumpbuffer.set("jump_in_cd", self.jump_cd)
        self.animator.set_trigger("jump")
        self.jumpbuffer.pop("jump")
        self.jumpbuffer.pop("on_ground")

    def update(self):
        super().update()

        if not(self.jumpbuffer.get("jump_in_cd")) and \
                self.jumpbuffer.get("jump") and \
                self.jumpbuffer.get("on_ground"):
            self.do_jump()

        self.jumpbuffer.update()

    def move(self, direction: Vector2):
        if not(self.jumpbuffer.get("move_in_cd")) and \
                self.jumpbuffer.get("on_ground"):

            self.jumpbuffer.set("move_in_cd", self.move_cd)

            direction.scale_to_length(self.move_speed)
            self.rigidbody.add_force(
                (direction.x, 0, direction.y), ForceMode.impulse)
            self.do_jump()

    def on_collide(self, collision: Collision):
        if collision.face is Face.down:
            self.jumpbuffer.set(
                "on_ground", self.can_jump_since_exit_ground_time)
        if not collision.gameobject:
            return
        if collision.gameobject.compare_tag(Tag.player):
            if collision.face in Face.around:
                target = collision.gameobject.get_component(
                    Character)
                
                attack_param = AttackParam(
                    self.collide_damage)
                attack_param.set_attacker(self)
                target.under_attack(attack_param)
