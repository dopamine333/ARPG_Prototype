from pygame import Surface, font
import pygame
from pygame.transform import scale
from pygame.image import load

from Scripts.Character.Character import Character
from Scripts.Character.Slime import Slime
from Scripts.Character.Hero import Hero
from Scripts.Character.CharacterBrain.PlayerController import PlayerController
from Scripts.Character.CharacterBrain.SlimeBrain import SlimeBrain

from Scripts.Animation.Animation import Animation
from Scripts.Animation.Animator import Animator

from Scripts.Graphic.Image import Image
from Scripts.Graphic.Render.SpriteRender import SpriteRender

from Scripts.Physics.RigidBody import RigidBody

from Scripts.Locals import CharacterID, PlayMode

from Scripts.GameObject.GameObject import GameObject


class CharacterFactory:
    def __init__(self) -> None:
        # TODO 更好的動畫載入方式
        self.hero_animation_clips: dict[str, list[Image]] = {}

        acts_and_center:dict[str,dict]={
            "air_attack":{
                1:(233,263),
                2:(233,263),
                3:(174,222),
                -1:(155,216)
            },
            "combo_attack1":{
                -1:(51,126),
            },
            "combo_attack2":{
                 0:(148,274),
                 -1:(220,266)
            },
            "combo_attack3":{
                -1:(47,422),
                },
            "dead":{
                -1:(206,210),
            },
            "fall":{
                -1:(90,183),

            },
            "idle":{
                -1:(34,118),
                },
            "jump":{
                0:(107,257),
                1:(103,245),
                2:(98,139),
                -1:(107,145)
                },
            "land":{
                -1:(44,164),
            },
            "run":{
                -1:(56,180)},
            "underattack":{
                -1:(128,199),
            }
        }
        

        for act,frame_center in acts_and_center.items():
            clip=[]
            i=0
            while True:
                try:
                    source=load(f"Arts\Character\hero\{act}\hero_{act}{str(i).zfill(2)}.png").convert_alpha()
                    image=Image(source,frame_center.get(i,frame_center[-1]))
                    clip.append(image)
                except:
                    print(act,i)
                    break
                i+=1
            self.hero_animation_clips[act]=clip


        '''for act in ["dead", "idle", "jump", "run"]:
            clip = []
            for i in range(1, 16):
                clip.append(Image(
                    scale(load(f"Arts\Character\hero\{act} ({i}).png"), (150, 150)).convert_alpha(), (30, 140)))
            self.hero_animation_clips[act] = clip
        
        for combo_attack in ["combo_attack1","combo_attack2","combo_attack3"]:
            clip=[]
            for i in range(5):
                f = font.SysFont(font.get_default_font(),(-abs(i-2)+3)*20)
                source=Surface((150,150),pygame.SRCALPHA)
                body=Surface((40, 120))
                body.fill((10, 207, 214))
                source.blit(body,(55,30))
                source.blit(f.render(combo_attack[-1],True,(255,255,255)),(70,50))
                clip.append(Image(source,(75,150)))
            self.hero_animation_clips[combo_attack] = clip'''
            


        self.slime_sprite_sheet = scale(
            load("Arts\Character\slime\Slime_Sprite_Sheet.png"), (687, 510)).convert_alpha()
        self.slime_jump_animation = Animation.generate_clip_use_sprite_sheet(
            self.slime_sprite_sheet, (20, 24), (64, 72), (30, 69), 9)
        self.slime_idle_animation = Animation.generate_clip_use_sprite_sheet(
            self.slime_sprite_sheet, (21, 105), (54, 63), (27, 45), 3)

    def create(self, characterID: CharacterID) -> Character:

        if characterID == CharacterID.slime:
            gameobject = GameObject()
            rigidbody = gameobject.add_component(RigidBody)
            slime = gameobject.add_component(Slime)
            render = gameobject.add_component(SpriteRender)
            animator = gameobject.add_component(Animator)
            idle = Animation()
            jump = Animation()
            animator.add_animations(idle, jump)
            animator.set_default_animation(idle)
            animator.add_trigger("jump")
            idle.set_clip(self.slime_idle_animation)
            jump.set_clip(self.slime_jump_animation)
            idle.set_speed(0.2)
            jump.set_speed(0.2)
            idle.set_play_mode(PlayMode.loop)
            idle.add_transition(jump, False, ("jump", True))
            jump.add_transition(idle, True)

            render.set_shadow_size((40, 40))
            rigidbody.set_collider((40, 30, 40), (30, 0, 30))
            brain = SlimeBrain()
            slime.set_brain(brain)
            return slime

        elif characterID == CharacterID.hero:
            ani: dict[str, Animation] = {} #animation

            for act, clip in self.hero_animation_clips.items():
                ani[act] = Animation()
                ani[act].set_clip(clip)
                ani[act].set_speed(0.35)
                '''if act in ["combo_attack1","combo_attack2","combo_attack3"]:
                    ani[act].set_speed(0.2)'''

            ani["dead"].set_speed(0.1)
            gameobject = GameObject()
            hero = gameobject.add_component(Hero)
            rigidbody = gameobject.add_component(RigidBody)
            render = gameobject.add_component(SpriteRender)
            animator = gameobject.add_component(Animator)
            
            animator.add_animations(*ani.values())
            animator.set_default_animation(ani["idle"])

            #["dead", "idle", "jump", "run"]
            animator.add_bool("running", "on_ground", "dead","complete_attack")
            animator.add_trigger("attack","underattack")
            ani["idle"].set_play_mode(PlayMode.loop)
            ani["run"].set_play_mode(PlayMode.loop)
            ani["fall"].set_play_mode(PlayMode.loop)

            ani["idle"].add_transition(ani["run"], False, ("running", True))
            ani["idle"].add_transition(ani["jump"], False, ("on_ground", False))

            ani["jump"].add_transition(ani["fall"],True)
            ani["fall"].add_transition(ani["land"],False,("on_ground",True))
            ani["land"].add_transition(ani["idle"], True)

            ani["jump"].add_transition(ani["air_attack"],False,("attack",True))
            ani["air_attack"].add_transition(ani["fall"],True)

            ani["run"].add_transition(ani["idle"], False, ("running", False))
            ani["run"].add_transition(ani["jump"], False, ("on_ground", False))

            ani["underattack"].add_transition(ani["idle"],True)

            ani["dead"].get_frame_event(14) + gameobject.destroy
            # TODO 註冊動畫事件應該在Character裡 還是在工廠裡
            ani["run"].get_frame_event(0) + hero.play_move_VFX_and_SFX
            ani["run"].get_frame_event(4) + hero.play_move_VFX_and_SFX

            #["combo_attack1","combo_attack2","combo_attack3"]

            ani["idle"].add_transition(ani["combo_attack1"],False,("attack",True))
            ani["run"].add_transition(ani["combo_attack1"],False,("attack",True))
            ani["underattack"].add_transition(ani["combo_attack1"],False,("attack",True))

            ani["combo_attack1"].add_transition(ani["jump"], False, ("on_ground", False))
            ani["combo_attack2"].add_transition(ani["jump"], False, ("on_ground", False))
            ani["combo_attack3"].add_transition(ani["jump"], False, ("on_ground", False))

            ani["combo_attack1"].add_transition(ani["idle"], True, ("on_ground", True))
            ani["combo_attack2"].add_transition(ani["idle"], True, ("on_ground", True))
            ani["combo_attack3"].add_transition(ani["idle"], True, ("on_ground", True))


            ani["combo_attack1"].add_transition(ani["combo_attack2"],False,("attack",True),("complete_attack",True))
            ani["combo_attack2"].add_transition(ani["combo_attack3"],False,("attack",True),("complete_attack",True))
            ani["combo_attack3"].add_transition(ani["idle"],True)

            complete_attack=lambda:animator.set_bool("complete_attack",True)
            new_attack=lambda:animator.set_bool("complete_attack",False)

            ani["combo_attack1"].get_frame_event(1) + hero.combo_attack_1 + complete_attack
            ani["combo_attack2"].get_frame_event(1) + hero.combo_attack_2 + complete_attack
            ani["combo_attack3"].get_frame_event(1) + hero.combo_attack_3 + complete_attack
            ani["air_attack"].get_frame_event(2) + hero.air_attack

            ani["combo_attack1"].get_frame_event(0) + new_attack
            ani["combo_attack2"].get_frame_event(0) + new_attack
            ani["combo_attack3"].get_frame_event(0) + new_attack


            for animation in ani.values():
                if animation==ani["dead"]:
                    continue
                animation.add_transition(ani["dead"], False, ("dead", True))
                animation.add_transition(ani["underattack"],False,("underattack",True))

            rigidbody.set_collider((40, 120, 40), (20, 0, 20))
            hero.set_brain(PlayerController())
            render.set_shadow_size((40, 40))
            return hero
