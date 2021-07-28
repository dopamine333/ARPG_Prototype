from Scripts.VisualEffectManager.VisualEffectManager import VisualEffectManager
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
from Scripts.Locals import Face, ForceMode, Layer, Tag, VisualEffectID
from Scripts.Physics.Box import Box
from pygame.image import load
from Scripts.Physics.RigidBody import RigidBody
from pygame import Vector2, Vector3
import pygame.transform


class Hero(Character):
    def __init__(self) -> None:
        super().__init__()
        self.jump_visualeffectID: VisualEffectID = None
        self.move_visualeffectID: VisualEffectID = None
        self.landing_visualeffectID: VisualEffectID = None
        self.attack_visualeffectID: VisualEffectID = None
        self.underattack_visualeffectID: VisualEffectID = None
        self.dead_visualeffectID: VisualEffectID = None

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

        

        self.animator = self.get_component(Animator)
        self.render = self.get_component(SpriteRender)

    def on_collide(self, collision: Collision):
        if collision.face is Face.down:
            if not self.jumpbuffer.get("on_ground"):
                self.play_visualeffect(self.landing_visualeffectID, self.get_bottom())
            self.jumpbuffer.set(
                "on_ground", self.can_jump_since_exit_ground_time)



    def jump(self):
        self.jumpbuffer.set("jump", self.can_jump_before_enter_ground_time)

    def do_jump(self):
        self.play_visualeffect(self.jump_visualeffectID,  self.get_bottom())

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

        self.play_visualeffect(self.move_visualeffectID, self.get_bottom())

    def dead(self):
        self.is_dead = True
        self.animator.set_bool("dead", True)
        self.play_visualeffect(self.dead_visualeffectID, self.position)

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

        self.play_visualeffect(
            self.attack_visualeffectID, self.position+offset)

    # TODO 使用樣板模式撥放動畫
    def under_attack(self, attack_param: AttackParam):
        if self.buffer.get("invincible"):
            return
        super().under_attack(attack_param)
        position = self.position+Vector3((random()-0.5)*self.rigidbody.collider.get_size().x,
                                         (random()-0.5) *
                                         self.rigidbody.collider.get_size().y,
                                         (random()-0.5)*self.rigidbody.collider.get_size().z)
        self.play_visualeffect(self.underattack_visualeffectID, position)

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

    def play_visualeffect(self, visualeffectID: VisualEffectID, position: Vector3):
        VisualEffectManager.Instance().play(visualeffectID, position)
