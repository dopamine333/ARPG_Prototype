from Scripts.Character.Character import Character
from Scripts.Animation.Transition import Transition
from Scripts.Animation.Animation import Animation
from pygame.transform import scale
from Scripts.Camera.CameraController import CameraController
from Scripts.Button.MouseManager import MouseManager
from Scripts.Physics.Physics import Physics
from Scripts.Button.Button import Button
from Scripts.Graphic.Render.Render import Render
from Scripts.Character.Slime import Slime
from Scripts.Character.Hero import Hero
from Scripts.GameObject.GameObject import GameObject
from Scripts.Graphic.Image import Image
from Scripts.Camera.Camera import Camera
from Scripts.Graphic.RenderManager import RenderManager
from Scripts.Physics.Box import Box
from Scripts.Locals import ButtonEvent, Face, Layer, PlayMode, Tag, VisualEffectID
from Scripts.Physics.Collider import Collider
from Scripts.Physics.RigidBody import RigidBody
from pygame.image import load
import pygame
from time import time
import Scripts.Scene.Scenes.MainMenuScene
from Scripts.Scene.Scenes.Scene import Scene
from pygame import Rect, Surface
from random import random
from Scripts.Character.CharacterBrain.PlayerController import PlayerController
from Scripts.Character.CharacterBrain.SlimeBrain import SlimeBrain
from Scripts.Graphic.Render.SpriteRender import SpriteRender
from Scripts.Animation.Animator import Animator
from os.path import join
from Scripts.Locals import CharacterID


class CharacterFactory:
    def __init__(self) -> None:
        #TODO 更好的動畫載入方式
        self.hero_animation_clips:dict[str,list[Image]]={}
        acts=["Dead","Idle","Jump","Run"]
        for act in acts:
            clip=[]
            for i in range(1,16):
                clip.append(Image(
                scale(load(f"Arts\Character\hero\{act} ({i}).png"),(150, 150)).convert_alpha(), (30, 140)))
            self.hero_animation_clips[act]=clip
        self.slime_sprite_sheet = scale( load("Arts\Character\slime\Slime_Sprite_Sheet.png"),(687, 510)).convert_alpha()
        self.slime_jump_animation=Animation.generate_clip_use_sprite_sheet(self.slime_sprite_sheet,(20,24),(64,72),(30,69),9)
        self.slime_idle_animation=Animation.generate_clip_use_sprite_sheet(self.slime_sprite_sheet,(21,105),(54,63),(27,45),3)
    def create(self, characterID: CharacterID)->Character:

        if characterID==CharacterID.Slime:
            gameobject = GameObject()
            rigidbody = gameobject.add_component(RigidBody)
            slime = gameobject.add_component(Slime)
            render = gameobject.add_component(SpriteRender)
            animator=gameobject.add_component(Animator)
            idle= Animation()
            jump= Animation()
            animator.add_animations(idle,jump)
            animator.set_default_animation(idle)
            animator.add_trigger("jump")
            idle.set_clip(self.slime_idle_animation)
            jump.set_clip(self.slime_jump_animation)
            idle.set_speed(0.2)
            jump.set_speed(0.2)
            idle.set_play_mode(PlayMode.loop)
            idle.add_transition(Transition(jump,False).add_condition(("jump",True)))
            jump.add_transition(Transition(idle,True))
            slime.jump_visualeffectID=VisualEffectID.slime_jump
            slime.move_visualeffectID=VisualEffectID.slime_move
            slime.attack_visualeffectID=VisualEffectID.slime_attack
            slime.landing_visualeffectID=VisualEffectID.slime_landing
            slime.underattack_visualeffectID=VisualEffectID.slime_underattack
            slime.dead_visualeffectID=VisualEffectID.slime_dead
            render.set_shadow_size((40, 40))
            rigidbody.set_collider(Collider((40, 30, 40), (30, 0, 30)))
            brain = SlimeBrain()
            slime.set_brain(brain)
            return slime
        elif characterID==CharacterID.Hero:
            animations:dict[str,Animation]={}
            for act,clip in self.hero_animation_clips.items():
                animations[act]=Animation()
                animations[act].set_clip(clip)
                animations[act].set_speed(0.5)
            animations["Dead"].set_speed(0.1)
            gameobject = GameObject()
            hero = gameobject.add_component(Hero)
            rigidbody = gameobject.add_component(RigidBody)
            render = gameobject.add_component(SpriteRender)
            animator=gameobject.add_component(Animator)
            animator.add_animations(*animations.values())
            animator.set_default_animation(animations["Idle"])
            animations["Dead"].attach(14,gameobject.destroy)
            animator.add_bool("running","on_ground","dead")
            animations["Idle"].set_play_mode(PlayMode.loop)
            animations["Jump"].set_play_mode(PlayMode.once)
            animations["Run"].set_play_mode(PlayMode.loop)
            animations["Dead"].set_play_mode(PlayMode.once)
            animations["Idle"].add_transition(Transition(animations["Run"],False).add_condition(("running",True)))
            animations["Idle"].add_transition(Transition(animations["Jump"],False).add_condition(("on_ground",False)))
            animations["Jump"].add_transition(Transition(animations["Idle"],False).add_condition(("on_ground",True)))
            animations["Run"].add_transition(Transition(animations["Idle"],False).add_condition(("running",False)))
            animations["Run"].add_transition(Transition(animations["Jump"],False).add_condition(("on_ground",False)))
            animations["Idle"].add_transition(Transition(animations["Dead"],False).add_condition(("dead",True)))
            animations["Jump"].add_transition(Transition(animations["Dead"],False).add_condition(("dead",True)))
            animations["Run"].add_transition(Transition(animations["Dead"],False).add_condition(("dead",True)))
            hero.jump_visualeffectID=VisualEffectID.hero_jump
            hero.move_visualeffectID=VisualEffectID.hero_move
            hero.attack_visualeffectID=VisualEffectID.hero_attack
            hero.landing_visualeffectID=VisualEffectID.hero_landing
            hero.underattack_visualeffectID=VisualEffectID.hero_underattack
            hero.dead_visualeffectID=VisualEffectID.hero_dead
            rigidbody.set_collider(Collider((40, 120, 40), (20, 0, 20)))
            hero.set_brain(PlayerController())
            render.set_shadow_size((40, 40))
            return hero