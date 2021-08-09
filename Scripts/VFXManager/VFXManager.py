from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Scripts.Character.Character import Character
from Scripts.Animation.Animation import Animation
from functools import cache
from Scripts.Tools.Singleton import Singleton
from Scripts.Animation.Animator import Animator
from random import choice, random
from Scripts.Locals import Tag, VFXID
from Scripts.Time.LifeTimer import LifeTimer
from Scripts.Graphic.Image import Image
from Scripts.Graphic.Render.SpriteRender import SpriteRender
from Scripts.GameObject.GameObject import GameObject
from Scripts.Physics import RigidBody
from pygame import Color, Surface, Vector2, Vector3, image, mouse
import pygame.font


class VFXManager(Singleton):
    def __init__(self) -> None:
        self.font = pygame.font.SysFont("Segoe Script", 40, True)
        #self.damagetext_dict: dict[int, dict[Tag, list[Image]]] = {}

    def play(self, vfxID: VFXID, position: Vector3):
        # FIXME 測試特效用 改為使用實際動畫
        text = {
            VFXID.hero_attack: "SWING",
            VFXID.hero_jump: "JUMP",
            VFXID.hero_move: choice(["Clip", "Clop"]),
            VFXID.hero_underattack: "OUCH!",
            VFXID.hero_dead: "AHHHHHHHHHHH",
            VFXID.hero_landing: "Thud",

            VFXID.slime_attack: "PA",
            VFXID.slime_jump: "DUANG",
            VFXID.slime_underattack: "DRIP",
            VFXID.slime_dead: "POP",
            VFXID.slime_landing: "Fizz",

            VFXID.finish_level: "YOU WIN!",
            VFXID.finish_checkpoint: "Clear Checkpoint!",
            VFXID.trigger_savepoint: "SavePoint Triggered",
            VFXID.trigger_checkpoint: "Start Fighting!",

            VFXID.goldsword_trigger: "DING!!",
            VFXID.goldsword_shake: choice(["clank!", "clang!"]),
        }
        size = {
            VFXID.hero_jump: 30,
            VFXID.hero_attack: 35,
            VFXID.hero_underattack: 60,
            VFXID.hero_dead: 65,

            VFXID.slime_attack: 30,
            VFXID.slime_underattack: 25,
            VFXID.slime_dead: 70,

            VFXID.finish_checkpoint: 100,
            VFXID.trigger_savepoint: 80,
            VFXID.trigger_checkpoint: 80,
            VFXID.finish_level: 110,

            VFXID.goldsword_trigger: 60,
            VFXID.goldsword_shake: 50,
        }
        WEITH = (255, 255, 255)
        GREY = (210, 210, 210)
        BLOOD = (250, 54, 0)
        DAEKBLOOD = (171, 3, 3)
        GOLD = (255, 203, 15)
        DARK = (75, 75, 75)
        BREEN = (36, 174, 47)
        DARKBREEN = (17, 73, 8)
        color = {
            VFXID.hero_jump: GREY,
            VFXID.hero_attack: WEITH,
            VFXID.hero_underattack: DAEKBLOOD,
            VFXID.hero_dead: DAEKBLOOD,

            VFXID.slime_attack: DARKBREEN,
            VFXID.slime_jump: DARKBREEN,
            VFXID.slime_underattack: DARKBREEN,
            VFXID.slime_dead: BREEN,
            VFXID.slime_landing: DARKBREEN,

            VFXID.finish_checkpoint: WEITH,
            VFXID.trigger_savepoint: WEITH,
            VFXID.trigger_checkpoint: WEITH,
            VFXID.finish_level: WEITH,

            VFXID.goldsword_trigger: GOLD,
            VFXID.goldsword_shake: GOLD,
        }
        if not vfxID in text:
            return
        effect = GameObject()
        render = effect.add_component(SpriteRender)
        font = pygame.font.SysFont("Segoe Script", size.get(vfxID, 15), True)
        effect.add_component(LifeTimer).set_lifetime(
            1.5 if not vfxID == VFXID.finish_level else 10)
        render.set_image(
            Image(font.render(text[vfxID], True, color.get(vfxID, DARK))))
        effect.set_position(position+Vector3(0, 0, 20))
        effect.instantiate()

    def play_UI(self):
        pass

    @cache
    def get_damagetext_clip(self, damage: int, defender_tag: Tag):
        '''if damage in self.damagetext_dict:
            if defender_tag in self.damagetext_dict[damage]:
                return self.damagetext_dict[damage][defender_tag]
        '''
        color = (171, 3, 3) if defender_tag == Tag.player else (245, 255, 253)
        clip = []
        for i in range(60):
            size = (i-60)*(-0.06 * i-0.7)
            # size=0.0025*(i-43.2)**3-1.461*(i-43.2)+55
            font = pygame.font.SysFont(
                "Segoe Script", int(size*(damage*0.1+1)), True)
            text = font.render(str(damage), True, color)
            clip.append(Image(text))
        #print(f"new damagetext {damage=} {defender_tag.name=}")
        return clip
        if not damage in self.damagetext_dict:
            self.damagetext_dict[damage] = {}
        self.damagetext_dict[damage][defender_tag] = clip
        return self.damagetext_dict[damage][defender_tag]

    def play_damagetext(self, damage: int, defender_tag: Tag, position: Vector3):
        damagetext = GameObject()
        animator = damagetext.add_component(Animator)
        render = damagetext.add_component(SpriteRender)
        animator.set_render(render)
        fading_away_animation = Animation()
        fading_away_animation.set_clip(
            self.get_damagetext_clip(damage, defender_tag))
        fading_away_animation.get_frame_event(59) + damagetext.destroy
        animator.set_default_animation(fading_away_animation)
        render.set_shadow_size((40, 40))
        damagetext.set_position(position)
        damagetext.instantiate()
