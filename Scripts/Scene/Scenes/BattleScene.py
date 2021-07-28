from Scripts.GameSystem.GameManager import GameManager
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
from Scripts.Locals import ButtonEvent, Face, Layer, PlayMode, Tag
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
class BattleScene(Scene):
    def scene_start(self):
        '''
        # region text gamemanager
        
        # region hero
        hero_image = Image(
            load( r"Arts\Character\hero.png").convert_alpha(), (25, 123))
        hero_animations:dict[str,Animation]={}
        acts=["Dead","Idle","Jump","Run"]
        for act in acts:
            clip=[]
            for i in range(1,16):
                clip.append(Image(
                scale(load(f"Arts\Character\hero\{act} ({i}).png"),(150, 150)).convert_alpha(), (30, 140)))
            a=Animation()
            a.set_clip(clip)
            a.set_speed(0.5)
            hero_animations[act]=a
        hero_animations["Dead"].set_speed(0.1)
        hero = GameObject()
        hero_hero = hero.add_component(Hero)
        hero_rigidbody = hero.add_component(RigidBody)
        hero_render = hero.add_component(SpriteRender)
        hero_animator=hero.add_component(Animator)
        hero_animator.add_animations(*hero_animations.values())
        hero_animator.set_default_animation(hero_animations["Idle"])
        hero_animations["Dead"].attach(14,hero.destroy)
        hero_animator.add_bool("running","on_ground","dead")
        hero_animations["Idle"].set_play_mode(PlayMode.loop)
        hero_animations["Jump"].set_play_mode(PlayMode.once)
        hero_animations["Run"].set_play_mode(PlayMode.loop)
        hero_animations["Dead"].set_play_mode(PlayMode.once)
        hero_animations["Idle"].add_transition(Transition(hero_animations["Run"],False).add_condition(("running",True)))
        hero_animations["Idle"].add_transition(Transition(hero_animations["Jump"],False).add_condition(("on_ground",False)))
        hero_animations["Jump"].add_transition(Transition(hero_animations["Idle"],False).add_condition(("on_ground",True)))
        hero_animations["Run"].add_transition(Transition(hero_animations["Idle"],False).add_condition(("running",False)))
        hero_animations["Run"].add_transition(Transition(hero_animations["Jump"],False).add_condition(("on_ground",False)))
        hero_animations["Idle"].add_transition(Transition(hero_animations["Dead"],False).add_condition(("dead",True)))
        hero_animations["Jump"].add_transition(Transition(hero_animations["Dead"],False).add_condition(("dead",True)))
        hero_animations["Run"].add_transition(Transition(hero_animations["Dead"],False).add_condition(("dead",True)))
        hero_rigidbody.set_collider(Collider((40, 120, 40), (20, 0, 20)))
        hero_hero.set_brain(PlayerController())
        hero_render.set_shadow_size((40, 40))
        hero.set_position((720, 100, 720))
        hero.set_tag(Tag.player)
        self.add_gameobject(hero)
        # endregion
 
        # region slime
        slime_image = Image(
            load(r"Arts\Character\slime.png").convert_alpha(), (40, 40))
        slime_sprite_sheet = scale( load("Arts\Character\slime\Slime_Sprite_Sheet.png"),(687, 510)).convert_alpha()
        for _ in range(15):
            slime = GameObject()
            slime_rigidbody = slime.add_component(RigidBody)
            slime_slime = slime.add_component(Slime)
            slime_render = slime.add_component(SpriteRender)
            slime_animator=slime.add_component(Animator)
            idle= Animation()
            jump= Animation()
            slime_animator.add_animations(idle,jump)
            slime_animator.set_default_animation(idle)
            slime_animator.add_trigger("jump")
            #TODO 新增讓動畫播完自動轉換的功能
            slime_animator.add_bool("true")
            slime_animator.set_bool("true",True)
            idle.use_sprite_sheet(slime_sprite_sheet,(21,105),(54,63),(27,45),3)
            jump.use_sprite_sheet(slime_sprite_sheet,(20,24),(64,72),(30,69),9)
            idle.set_speed(0.2)
            jump.set_speed(0.2)
            idle.set_play_mode(PlayMode.loop)
            idle.add_transition(Transition(jump,False).add_condition(("jump",True)))
            jump.add_transition(Transition(idle,True).add_condition(("true",True)))
            slime_render.set_shadow_size((40, 40))
            slime_rigidbody.set_collider(Collider((40, 30, 40), (30, 0, 30)))
            slime.set_position((random()*1280, random()*400, random()*1280))
            slime_brain = SlimeBrain()
            slime_brain.set_target(hero_hero)
            slime_slime.set_brain(slime_brain)
            slime.set_tag(Tag.enemy)

            self.add_gameobject(slime)
        # endregion
        # endregion
        '''
        # region obstacle
        for _ in range(8):
            size = random()*150+50
            obstacle_source = Surface(
                (size, size), pygame.SRCALPHA).convert_alpha()
            obstacle_source.fill((random()*255, random()*200, random()*200))
            obstacle = GameObject()
            obstacle_render = obstacle.add_component(SpriteRender)
            obstacle_rigidbody = obstacle.add_component(RigidBody)
            obstacle_rigidbody.set_frozen(True)
            obstacle_rigidbody.set_collider(
                Collider((size, size, 20), (size/2, 0, 10)))
            obstacle_render.set_image(Image(obstacle_source, (size/2, size)))
            obstacle_render.set_shadow_size((size, 20))
            obstacle.set_position((random()*1280, 0, random()*1280))

            self.add_gameobject(obstacle)
        # endregion
        
        # region to_mainmenu_button

        to_mainmenu_button_source = load(
            r"Arts\BattleMenu\to_mainmenu.png").convert_alpha()
        to_mainmenu_button_size = to_mainmenu_button_source.get_size()
        to_mainmenu_button = GameObject()
        to_mainmenu_button_render = to_mainmenu_button.add_component(Render)
        to_mainmenu_button_button = to_mainmenu_button.add_component(Button)
        to_mainmenu_button_render.set_image(Image(to_mainmenu_button_source))
        to_mainmenu_button_render.set_layer(Layer.UI)
        to_mainmenu_button_button.set_button_size(to_mainmenu_button_size)
        to_mainmenu_button.set_position((1212, 665, 0))

        to_mainmenu_button_button.attach(ButtonEvent.up, self.to_mainmenu)
        self.add_gameobject(to_mainmenu_button)
        # endregion
        
        #region camera
        camera=GameObject()
        camera_camera=camera.add_component(Camera)
        camera_controller=camera.add_component(CameraController)
        #camera_controller.set_target(hero)
        camera_controller.set_follow_axis(y=False)
        camera_controller.set_offset((0,100,-100))
        camera_camera.set_activity_rect(Rect(-500,-500,2000,2000))
        camera_camera.set_shadow_color((10,10,50,50))
        self.add_gameobject(camera)
        #endregion



        RenderManager.set_camera(camera_camera)
        Physics.set_activity_box(Box((1280, 720, 1280), (640, 360, 640)))

        gamemanager=GameObject()
        from Data.LevelData import LevelData1
        gamemanager.add_component(GameManager).levelsystem.add_level(LevelData1.read())
        self.add_gameobject(gamemanager)

    def scene_update(self):
        MouseManager.update()
        Physics.update()

    def scene_end(self):
        RenderManager.set_camera(None)

    def to_mainmenu(self):
        self.change_scene(Scripts.Scene.Scenes.MainMenuScene.MainMenuScene)
