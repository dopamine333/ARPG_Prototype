from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Scripts.Character.Character import Character
from Scripts.Animation.Animation import Animation
from functools import cache
from Scripts.Tools.Singleton import Singleton
from Scripts.Animation.Animator import Animator
from random import random
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
        self.font=pygame.font.SysFont("Segoe Script", 40, True)
        #self.damagetext_dict: dict[int, dict[Tag, list[Image]]] = {}

    def play(self, vfxID: VFXID, position: Vector3):
        #FIXME 測試特效用 改為使用實際動畫
        effect = GameObject()
        render = effect.add_component(SpriteRender)
        effect.add_component(LifeTimer).set_lifetime(1)
        render.set_image(Image(self.font.render(str(vfxID.name),True,(255,255,255))))
        effect.set_position(position)
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
        return clip
        if not damage in self.damagetext_dict:
            self.damagetext_dict[damage] = {}
        self.damagetext_dict[damage][defender_tag] = clip
        print("new text", damage, defender_tag)
        return self.damagetext_dict[damage][defender_tag]

    def play_damagetext(self, damage: int, defender_tag: Tag, position: Vector3):
        damagetext = GameObject()
        animator = damagetext.add_component(Animator)
        render = damagetext.add_component(SpriteRender)
        animator.set_render(render)
        fading_away_animation = Animation()
        fading_away_animation.set_clip(self.get_damagetext_clip(damage,defender_tag))
        fading_away_animation.attach(59, damagetext.destroy)
        animator.set_default_animation(fading_away_animation)
        render.set_shadow_size((40, 40))
        damagetext.set_position(position)
        damagetext.instantiate()
