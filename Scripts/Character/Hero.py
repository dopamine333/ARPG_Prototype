from pygame.transform import rotozoom
from Scripts.Attack.UnderAttackInterface import UnderAttackInterface
from Scripts.Attack.AttackParam import AttackParam

from Scripts.AudioManager.AudioManager import AudioManger
from Scripts.VFXManager.VFXManager import VFXManager

from Scripts.Physics.Collision import Collision
from Scripts.Physics.Physics import Physics
from Scripts.Physics.Box import Box

from Scripts.Animation.Animator import Animator
from Scripts.Graphic.Render.SpriteRender import SpriteRender
from Scripts.Graphic.Image import Image
from Scripts.Graphic.RenderManager import RenderManager

from Scripts.Character.Character import Character
from Scripts.Locals import Face, ForceMode, SFXID, Tag, VFXID
from random import random
from pygame.image import load
from pygame import Surface, Vector2, Vector3


class Hero(Character):

    def __init__(self):
        super().__init__()

        sword_flash_source = load(
            r"Arts\Character\sword_flash.png").convert_alpha()
        self.max_hp = 10
        self.jump_force = 2500
        self.dash_force = 1000
        self.move_speed = 1728

        self.face = Face.right
        self.can_jump_since_exit_ground_time = 0.5
        self.can_jump_before_enter_ground_time = 0.05

        # TODO 完成武器類別
        self.sword_damage = 3
        self.sword_force = Vector3(1000, 1200, 0)
        self.sword_flash_image1 = Image(sword_flash_source, Vector2(45, 44))
        self.sword_flash_image2 = Image(rotozoom(sword_flash_source,0,1.3), Vector2(58.5, 57.2))
        self.sword_flash_image3 = Image(rotozoom(sword_flash_source,0,1.6), Vector2(72, 70.4))
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

        self.animator: Animator = None
        self.render: SpriteRender = None

    # region override Character

    def awake(self):
        super().awake()
        self.animator = self.get_component(Animator)
        self.render = self.get_component(SpriteRender)
        self.rigidbody.set_damp(0.92)

    def update(self):
        if self.is_dead:
            return
        super().update()

        self.animator.set_bool("on_ground", self.is_on_ground())
        self.animator.set_bool(
            "running", self.rigidbody.acceleration.length_squared() > 1)

        if self.buffer.get("jump") and self.is_on_ground():
            self.do_jump()
            self.buffer.pop("jump")
            self.buffer.pop("on_ground")

        self.buffer.update()

        self.render.set_face(self.face)
    
    def on_collide(self, collision: Collision):
        # 如果下方碰撞
        if collision.face is Face.down:
            if not self.is_on_ground():
                self.on_landing()
            self.on_ground()

    def dead(self):
        self.is_dead = True
        # FIXME 死亡後屍體因為關卡重設而卡住
        self.rigidbody.set_frozen(True)
        self.animator.set_bool("dead", True)
        self.play_VFX(self.dead_VFXID, self.get_top())
        self.play_SFX(self.dead_SFXID)

    # TODO 使用樣板模式撥放動畫
    def take_damage(self, attack_param: AttackParam):
        super().take_damage(attack_param)
        position = self.position+Vector3((random()-0.5)*self.rigidbody.collider.get_size().x,
                                         random()*self.rigidbody.collider.get_size().y,
                                         (random()-0.5)*self.rigidbody.collider.get_size().z)
        self.play_VFX(self.underattack_VFXID, position)
        self.play_SFX(self.underattack_SFXID)

    # endregion

    # region Hero behaviour
    def is_face_left(self):
        return self.face is Face.left

    def is_on_ground(self):
        return self.buffer.get("on_ground")

    def on_ground(self):
        self.buffer.set("on_ground", self.can_jump_since_exit_ground_time)

    def on_landing(self):
        self.play_VFX(self.landing_VFXID, self.get_bottom())
        self.play_SFX(self.landing_SFXID)

    def do_jump(self):
        self.play_VFX(self.jump_VFXID,  self.get_bottom())
        self.play_SFX(self.jump_SFXID)

        self.rigidbody.add_force((0, self.jump_force, 0), ForceMode.impulse)
        self.animator.set_trigger("jump")

    def do_attack(self, size: Vector3, offset: Vector3, damage: int, force: Vector3):
        if self.is_face_left():
            offset.x *= -1
            force.x *= -1
        box = Box(size, self.position+offset)
        rigidbodies = Physics.overlap_box(box)
        for rigidbody in rigidbodies:
            if rigidbody.compare_tag(Tag.enemy | Tag.interactable):
                target = rigidbody.get_component(UnderAttackInterface)
                param = AttackParam(damage, force)
                param.set_attacker(self)
                target.under_attack(param)

    # endregion

    # region control by Brain

    def move(self, direction: Vector2):
        if direction.x > 0:
            self.face = Face.right
        elif direction.x < 0:
            self.face = Face.left
        direction.scale_to_length(self.move_speed)
        self.rigidbody.add_force(
            (direction.x, 0, direction.y), ForceMode.force)

    def attack(self):
        self.animator.set_trigger("attack")

    def jump(self):
        self.buffer.set("jump", self.can_jump_before_enter_ground_time)


    # endregion

    # region Animation event

    #FIXME 改成真正攻擊的參數
    def combo_attack_1(self):

        damage = 1
        force = Vector3(400, 1500, 0)
        size = Vector3(150, 60, 200)
        offset = Vector3(100, 60, 0)
        self.do_attack(size,offset,damage,force)

        if self.is_face_left():
            image=self.sword_flash_image1.flip(True,False)
        else:
            image=self.sword_flash_image1

        RenderManager.camera.draw(image, self.position+offset)

        #self.play_VFX(self.attack_VFXID, self.position+offset)
        self.play_SFX(self.attack_SFXID)

    
    def combo_attack_2(self):

        damage = 1
        force = Vector3(600, 1800, 0)
        size = Vector3(180, 70, 240)
        offset = Vector3(120, 60, 0)
        self.do_attack(size,offset,damage,force)
        surface=Surface(size.xy)
        surface.fill((150,150,0))


        if self.is_face_left():
            image=self.sword_flash_image2.flip(True,False)
        else:
            image=self.sword_flash_image2

        RenderManager.camera.draw(image, self.position+offset)

        #self.play_VFX(self.attack_VFXID, self.position+offset)
        self.play_SFX(self.attack_SFXID)
    
    def combo_attack_3(self):

        damage = 2
        force = Vector3(600, 2700, 0)
        size = Vector3(250, 200, 350)
        offset = Vector3(150, 60, 0)
        self.do_attack(size,offset,damage,force)
        surface=Surface(size.xy)
        surface.fill((150,150,150))


        if self.is_face_left():
            image=self.sword_flash_image3.flip(True,False)
        else:
            image=self.sword_flash_image3

        RenderManager.camera.draw(image, self.position+offset)

        #self.play_VFX(self.attack_VFXID, self.position+offset)
        self.play_SFX(self.attack_SFXID)

    def play_move_VFX_and_SFX(self):
        self.play_SFX(self.move_SFXID)
        self.play_VFX(self.move_VFXID, self.get_bottom())

    # endregion

    # region for juice

    def get_bottom(self):
        bottom = self.position.xyz
        bottom.y = self.rigidbody.get_surface(Face.down)
        return bottom

    def get_top(self):
        bottom = self.position.xyz
        bottom.y = self.rigidbody.get_surface(Face.up)
        return bottom

    def play_VFX(self, vfxID: VFXID, position: Vector3):
        VFXManager.Instance().play(vfxID, position)

    def play_SFX(self, sfxID: SFXID):
        AudioManger.Instance().play_SFX(sfxID)

    # endregion
