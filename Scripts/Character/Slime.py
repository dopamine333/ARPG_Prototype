
from Scripts.AudioManager.AudioManager import AudioManger
from Scripts.VFXManager.VFXManager import VFXManager
from Scripts.Tools.Buffer import Buffer
from Scripts.Animation.Animator import Animator
from enum import Flag
from Scripts.Locals import Face, ForceMode, SFXID, Tag, VFXID
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
        self.invincible_time = 0
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

        self.jump_VFXID=VFXID.slime_jump
        self.landing_VFXID=VFXID.slime_landing
        self.attack_VFXID=VFXID.slime_attack
        self.underattack_VFXID=VFXID.slime_underattack
        self.dead_VFXID=VFXID.slime_dead

        self.jump_SFXID=SFXID.slime_jump
        self.landing_SFXID=SFXID.slime_landing
        #self.attack_SFXID=SFXID.slime_attack
        self.underattack_SFXID=SFXID.slime_underattack
        self.dead_SFXID=SFXID.slime_dead

        self.animator: Animator = self.get_component(Animator)

    def jump(self):
        self.jumpbuffer.set("jump", self.can_jump_before_enter_ground_time)

    def do_jump(self):
        self.rigidbody.add_force((0, self.jump_force, 0), ForceMode.impulse)
        self.jumpbuffer.set("jump_in_cd", self.jump_cd)
        self.animator.set_trigger("jump")
        self.jumpbuffer.pop("jump")
        self.jumpbuffer.pop("on_ground")

        self.play_VFX(self.jump_VFXID, self.get_bottom())
        self.play_SFX(self.jump_SFXID)
        

    def get_bottom(self):
        bottom = self.position.xyz
        bottom.y = self.rigidbody.get_surface(Face.down)
        return bottom

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

        

    def under_attack(self, attack_param: AttackParam):
        #FIXME 降under_attack街口、實際受傷、播放動畫分開
        if self.buffer.get("invincible"):
            return
        position = self.position+Vector3((random()-0.5)*self.rigidbody.collider.get_size().x,
                                         (random()-0.5) *
                                         self.rigidbody.collider.get_size().y,
                                         (random()-0.5)*self.rigidbody.collider.get_size().z)
        self.play_VFX(self.underattack_VFXID, position)
        self.play_SFX(self.underattack_SFXID)

        super().under_attack(attack_param)
    def dead(self):
        self.is_dead=True
        self.play_VFX(self.dead_VFXID, self.position)
        self.play_SFX(self.dead_SFXID)

    def on_collide(self, collision: Collision):
        if collision.face is Face.down:
            if not self.jumpbuffer.get("on_ground"):
                self.on_landing()
            self.jumpbuffer.set(
            "on_ground", self.can_jump_since_exit_ground_time)
        if not collision.gameobject:
            return
        if collision.gameobject.compare_tag(Tag.player):
            if collision.face in Face.around:
                self.attack(collision.gameobject.get_component(Character))

    def on_landing(self):
        self.play_VFX(self.landing_VFXID, self.get_bottom())
        self.play_SFX(self.landing_SFXID)  
        self.jumpbuffer.set(
            "on_ground", self.can_jump_since_exit_ground_time)

    def attack(self, target: Character):
        attack_param = AttackParam(self.collide_damage)
        attack_param.set_attacker(self)
        target.under_attack(attack_param)

        position = (target.position+self.position)*0.5
        self.play_VFX(self.attack_VFXID, position)
        #self.play_SFX(self.attack_SFXID)


    def play_VFX(self, VFXID: VFXID, position: Vector3):
        VFXManager.Instance().play(VFXID, position)
    def play_SFX(self,sfxID:SFXID):
        AudioManger.Instance().play_SFX(sfxID)