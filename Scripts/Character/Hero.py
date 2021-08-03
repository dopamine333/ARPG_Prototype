from Scripts.AudioManager.AudioManager import AudioManger
from Scripts.VFXManager.VFXManager import VFXManager
from Scripts.Tools.Buffer import Buffer
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
from Scripts.Locals import Face, ForceMode, Layer, SFXID, Tag, VFXID
from Scripts.Physics.Box import Box
from pygame.image import load
from Scripts.Physics.RigidBody import RigidBody
from pygame import Vector2, Vector3
import pygame.transform


class Hero(Character):

    def start(self):
        self.max_hp = 10
        super().start()

        sword_flash_source = load(
            r"Arts\Character\sword_flash.png").convert_alpha()
        self.jump_force = 2500
        self.dash_force = 1000
        self.move_speed = 1728
        self.rigidbody.damp = 0.92

        self.face = Face.right
        self.jumpbuffer = Buffer()
        self.can_jump_since_exit_ground_time = 0.5
        self.can_jump_before_enter_ground_time = 0.05

        # TODO 完成武器類別
        self.sword_damage = 3
        self.sword_force = Vector3(1000, 1200, 0)
        self.sword_flash_image = Image(sword_flash_source, Vector2(45, 44))
        self.sword_flash_box_size = Vector3(100, 60, 100)
        self.sword_flash_offset = Vector3(100, 60, 0)

        self.jump_VFXID = VFXID.hero_jump
        self.move_VFXID = VFXID.hero_move
        self.landing_VFXID = VFXID.hero_landing
        self.attack_VFXID = VFXID.hero_attack
        self.underattack_VFXID = VFXID.hero_underattack
        self.dead_VFXID = VFXID.hero_dead

        self.jump_SFXID = SFXID.hero_jump
        self.move_SFXID = SFXID.hero_move
        self.landing_SFXID = SFXID.hero_landing
        self.attack_SFXID = SFXID.hero_attack
        self.underattack_SFXID = SFXID.hero_underattack
        self.dead_SFXID = SFXID.hero_dead

        self.animator = self.get_component(Animator)
        self.render = self.get_component(SpriteRender)

    def on_collide(self, collision: Collision):
        if collision.face is Face.down:
            if not self.jumpbuffer.get("on_ground"):
                self.on_landing()
            self.jumpbuffer.set(
            "on_ground", self.can_jump_since_exit_ground_time)
    def on_landing(self):
        self.play_VFX(self.landing_VFXID, self.get_bottom())
        self.play_SFX(self.landing_SFXID)
        

    def play_move_VFX_and_SFX(self):
        self.play_SFX(self.move_SFXID)
        self.play_VFX(self.move_VFXID, self.get_bottom())

    def jump(self):
        self.jumpbuffer.set("jump", self.can_jump_before_enter_ground_time)

    def do_jump(self):
        self.play_VFX(self.jump_VFXID,  self.get_bottom())
        self.play_SFX(self.jump_SFXID)

        self.rigidbody.add_force((0, self.jump_force, 0), ForceMode.impulse)
        self.animator.set_trigger("jump")

    def get_bottom(self):
        bottom = self.position.xyz
        bottom.y = self.rigidbody.get_surface(Face.down)
        return bottom

    def move(self, direction: Vector2):
        if direction.x > 0:
            self.face = Face.right
        elif direction.x < 0:
            self.face = Face.left
        direction.scale_to_length(self.move_speed)
        self.rigidbody.add_force(
            (direction.x, 0, direction.y), ForceMode.force)

    def dead(self):
        self.is_dead = True
        self.animator.set_bool("dead", True)
        self.play_VFX(self.dead_VFXID, self.position)
        self.play_SFX(self.dead_SFXID)

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

        self.play_VFX(
            self.attack_VFXID, self.position+offset)
        self.play_SFX(self.attack_SFXID)

    # TODO 使用樣板模式撥放動畫
    def under_attack(self, attack_param: AttackParam):
        if self.buffer.get("invincible"):
            return
        super().under_attack(attack_param)
        position = self.position+Vector3((random()-0.5)*self.rigidbody.collider.get_size().x,
                                         (random()-0.5) *
                                         self.rigidbody.collider.get_size().y,
                                         (random()-0.5)*self.rigidbody.collider.get_size().z)
        self.play_VFX(self.underattack_VFXID, position)
        self.play_SFX(self.underattack_SFXID)

    def update(self):
        if self.is_dead:
            return
        super().update()

        self.animator.set_bool("on_ground", self.jumpbuffer.get("on_ground"))
        self.animator.set_bool(
            "running", self.rigidbody.acceleration.length_squared() > 1)

        if self.jumpbuffer.get("jump") and self.jumpbuffer.get("on_ground"):
            self.do_jump()
            self.jumpbuffer.pop("jump")
            self.jumpbuffer.pop("on_ground")

        self.jumpbuffer.update()

        self.render.set_face(self.face)
        # print(self.animator.current_animation.frame)

    def play_VFX(self, vfxID: VFXID, position: Vector3):
        VFXManager.Instance().play(vfxID, position)

    def play_SFX(self, sfxID: SFXID):
        AudioManger.Instance().play_SFX(sfxID)
