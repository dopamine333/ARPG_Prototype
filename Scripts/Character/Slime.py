
from Scripts.Attack.UnderAttackInterface import UnderAttackInterface
from Scripts.Attack.AttackParam import AttackParam

from Scripts.AudioManager.AudioManager import AudioManger
from Scripts.VFXManager.VFXManager import VFXManager
from Scripts.Animation.Animator import Animator
from Scripts.Character.Character import Character
from Scripts.Physics.Collision import Collision

from Scripts.Locals import Face, ForceMode, SFXID, Tag, VFXID
from random import random
from pygame import Vector2, Vector3


class Slime(Character):

    def __init__(self) -> None:
        super().__init__()
        self.max_hp = 10
        self.invincible_time = 0

        self.jump_force = 2800
        self.move_speed = 1100

        self.can_jump_since_exit_ground_time = 0.05
        self.can_jump_before_enter_ground_time = 0.05

        self.move_cd = 4+0.8*random()
        self.jump_cd = 1.5

        self.collide_damage = 2

        self.jump_VFXID = VFXID.slime_jump
        self.land_VFXID = VFXID.slime_land
        self.attack_VFXID = VFXID.slime_attack
        self.underattack_VFXID = VFXID.slime_underattack
        self.dead_VFXID = VFXID.slime_dead

        self.jump_SFXID = SFXID.slime_jump
        self.land_SFXID = SFXID.slime_land
        # self.attack_SFXID=SFXID.slime_attack
        self.underattack_SFXID = SFXID.slime_underattack
        self.dead_SFXID = SFXID.slime_dead

        self.animator: Animator = None

    def awake(self):
        super().awake()
        self.animator = self.get_component(Animator)
        self.rigidbody.set_damp(0.93)

    def jump(self):
        self.buffer.set("jump", self.can_jump_before_enter_ground_time)

    def do_jump(self):
        self.rigidbody.add_force((0, self.jump_force, 0), ForceMode.impulse)
        self.buffer.set("jump_in_cd", self.jump_cd)
        self.animator.set_trigger("jump")
        self.buffer.pop("jump")
        self.buffer.pop("on_ground")

        self.play_VFX(self.jump_VFXID, self.get_bottom())
        self.play_SFX(self.jump_SFXID)

    def get_bottom(self):
        bottom = self.position.xyz
        bottom.y = self.rigidbody.get_surface(Face.down)
        return bottom

    def update(self):
        super().update()

        if not(self.buffer.get("jump_in_cd")) and \
                self.buffer.get("jump") and \
                self.buffer.get("on_ground"):
            self.do_jump()

        self.buffer.update()

    def move(self, direction: Vector2):
        if not(self.buffer.get("move_in_cd")) and \
                self.buffer.get("on_ground"):

            self.buffer.set("move_in_cd", self.move_cd)

            direction.scale_to_length(self.move_speed)
            self.rigidbody.add_force(
                (direction.x, 0, direction.y), ForceMode.impulse)
            self.do_jump()

    def take_damage(self, attack_param: AttackParam):
        super().take_damage(attack_param)
        position = self.position+Vector3((random()-0.5)*self.rigidbody.collider.get_size().x,
                                         random() * self.rigidbody.collider.get_size().y,
                                         (random()-0.5)*self.rigidbody.collider.get_size().z)
        self.play_VFX(self.underattack_VFXID, position)
        self.play_SFX(self.underattack_SFXID)

    def dead(self):
        self.is_dead = True
        self.play_VFX(self.dead_VFXID, self.position)
        self.play_SFX(self.dead_SFXID)

    def on_collide(self, collision: Collision):
        if collision.face is Face.down:
            if not self.buffer.get("on_ground"):
                self.on_land()
            self.buffer.set(
                "on_ground", self.can_jump_since_exit_ground_time)
        if not collision.gameobject:
            return
        if collision.gameobject.compare_tag(Tag.player):
            if collision.face in Face.around:
                self.attack(collision.gameobject.get_component(
                    UnderAttackInterface))

    def on_land(self):
        self.play_VFX(self.land_VFXID, self.get_bottom())
        self.play_SFX(self.land_SFXID)
        self.buffer.set(
            "on_ground", self.can_jump_since_exit_ground_time)

    def attack(self, target: Character):
        attack_param = AttackParam(self.collide_damage)
        attack_param.set_attacker(self)
        target.under_attack(attack_param)

        position = (target.position+self.position)*0.5
        self.play_VFX(self.attack_VFXID, position)
        # self.play_SFX(self.attack_SFXID)

    def play_VFX(self, VFXID: VFXID, position: Vector3):
        VFXManager.Instance().play(VFXID, position)

    def play_SFX(self, sfxID: SFXID):
        AudioManger.Instance().play_SFX(sfxID)
