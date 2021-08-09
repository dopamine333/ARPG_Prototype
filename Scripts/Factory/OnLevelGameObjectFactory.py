import pygame
from Scripts.Level.GoldSword import GoldSword
from math import degrees
from pygame import Surface
from Scripts.Locals import OnLevelGameObjectID, Tag

from pygame.transform import rotate

from Scripts.Animation.Animation import Animation
from Scripts.Animation.Animator import Animator

from Scripts.Graphic.Image import Image
from Scripts.Graphic.Render.SpriteRender import SpriteRender

from Scripts.Physics.RigidBody import RigidBody

from Scripts.GameObject.GameObject import GameObject


class OnLevelGameObjectFactory:
    def create(self, onlevelgameobjectID: OnLevelGameObjectID):
        if onlevelgameobjectID == OnLevelGameObjectID.goldsword:
            gameobject = GameObject()
            animator = gameobject.add_component(Animator)
            rigidbody = gameobject.add_component(RigidBody)
            render = gameobject.add_component(SpriteRender)
            goldsword = gameobject.add_component(GoldSword)
            stone = Animation()
            gold = Animation()
            trigger = Animation()
            shake = Animation()
            animator.add_animations(stone, gold, trigger, shake)
            animator.set_default_animation(stone)
            animator.add_trigger("trigger", "shake")

            # FIXME 實作金劍動畫
            GOLD = (255, 203, 15)
            stone_surface = Surface((50, 70)).convert()
            stone_surface.fill((64, 64, 64))
            stone.set_clip([Image(stone_surface, (25, 70))])

            gold_surface = Surface((50, 100)).convert()
            gold_surface.fill(GOLD)
            gold.set_clip([Image(gold_surface, (25, 100))])

            trigger_clip = []
            for i in range(60):
                trigger_surface = Surface((50+i*0.2, 100+i)).convert()
                trigger_surface.fill(GOLD)
                trigger_clip.append(Image(trigger_surface, (25+i*0.1, 100+i)))
            trigger.set_clip(trigger_clip)

            shake_clip = []
            shake_surface = Surface((50, 100), pygame.SRCALPHA)
            shake_surface.fill(GOLD)
            from math import sin
            for i in range(60):
                angle = sin(degrees(i*0.005))*30
                rotated_shake_surface = rotate(shake_surface, angle)
                rotated_shake_surface.get_rect().midbottom = rotated_shake_surface.get_rect().midbottom
                shake_clip.append(
                    Image(rotated_shake_surface, rotated_shake_surface.get_rect().midbottom))
            shake.set_clip(shake_clip)

            stone.add_transition(trigger, False, ("trigger", True))
            trigger.add_transition(gold, True)
            gold.add_transition(shake, False, ("shake", True))
            shake.add_transition(gold, True)
            shake.add_transition(shake, False, ("shake", True))

            rigidbody.set_frozen(True)
            rigidbody.set_collider((45, 70, 20), (22.5, 0, 10))
            render.set_shadow_size((45, 20))
            gameobject.set_tag(Tag.interactable)
            return goldsword
