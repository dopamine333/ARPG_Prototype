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
        for act in ["Dead", "Idle", "Jump", "Run"]:
            clip = []
            for i in range(1, 16):
                clip.append(Image(
                    scale(load(f"Arts\Character\hero\{act} ({i}).png"), (150, 150)).convert_alpha(), (30, 140)))
            self.hero_animation_clips[act] = clip
        
        for combo_attack in ["ComboAttack1","ComboAttack2","ComboAttack3"]:
            clip=[]
            for i in range(5):
                f = font.SysFont(font.get_default_font(),(-abs(i-2)+3)*20)
                source=Surface((150,150),pygame.SRCALPHA)
                body=Surface((40, 120))
                body.fill((10, 207, 214))
                source.blit(body,(55,30))
                source.blit(f.render(combo_attack[-1],True,(255,255,255)),(70,50))
                clip.append(Image(source,(75,150)))
            self.hero_animation_clips[combo_attack] = clip
            


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
                ani[act].set_speed(0.5)
                if act in ["ComboAttack1","ComboAttack2","ComboAttack3"]:
                    ani[act].set_speed(0.2)

            ani["Dead"].set_speed(0.1)
            gameobject = GameObject()
            hero = gameobject.add_component(Hero)
            rigidbody = gameobject.add_component(RigidBody)
            render = gameobject.add_component(SpriteRender)
            animator = gameobject.add_component(Animator)
            
            animator.add_animations(*ani.values())
            animator.set_default_animation(ani["Idle"])

            #["Dead", "Idle", "Jump", "Run"]
            animator.add_bool("running", "on_ground", "dead")
            ani["Idle"].set_play_mode(PlayMode.loop)
            ani["Run"].set_play_mode(PlayMode.loop)

            ani["Idle"].add_transition(ani["Run"], False, ("running", True))
            ani["Idle"].add_transition(ani["Jump"], False, ("on_ground", False))
            ani["Jump"].add_transition(ani["Idle"], False, ("on_ground", True))
            ani["Run"].add_transition(ani["Idle"], False, ("running", False))
            ani["Run"].add_transition(ani["Jump"], False, ("on_ground", False))
            ani["Idle"].add_transition(ani["Dead"], False, ("dead", True))
            ani["Jump"].add_transition(ani["Dead"], False, ("dead", True))
            ani["Run"].add_transition(ani["Dead"], False, ("dead", True))

            ani["Dead"].get_frame_event(14) + gameobject.destroy
            # TODO 註冊動畫事件應該在Character裡 還是在工廠裡
            ani["Run"].get_frame_event(0) + hero.play_move_VFX_and_SFX
            ani["Run"].get_frame_event(8) + hero.play_move_VFX_and_SFX

            #["ComboAttack1","ComboAttack2","ComboAttack3"]
            animator.add_trigger("attack")
            animator.add_bool("complete_attack")
            ani["Idle"].add_transition(ani["ComboAttack1"],False,("attack",True))
            ani["Run"].add_transition(ani["ComboAttack1"],False,("attack",True))

            ani["ComboAttack1"].add_transition(ani["Jump"], False, ("on_ground", False))
            ani["ComboAttack2"].add_transition(ani["Jump"], False, ("on_ground", False))
            ani["ComboAttack3"].add_transition(ani["Jump"], False, ("on_ground", False))

            ani["ComboAttack1"].add_transition(ani["Idle"], True, ("on_ground", True))
            ani["ComboAttack2"].add_transition(ani["Idle"], True, ("on_ground", True))
            ani["ComboAttack3"].add_transition(ani["Idle"], True, ("on_ground", True))

            ani["ComboAttack1"].add_transition(ani["Dead"], False, ("dead", True))
            ani["ComboAttack2"].add_transition(ani["Dead"], False, ("dead", True))
            ani["ComboAttack3"].add_transition(ani["Dead"], False, ("dead", True))

            ani["ComboAttack1"].add_transition(ani["ComboAttack2"],False,("attack",True),("complete_attack",True))
            ani["ComboAttack2"].add_transition(ani["ComboAttack3"],False,("attack",True),("complete_attack",True))
            ani["ComboAttack3"].add_transition(ani["Idle"],True)

            complete_attack=lambda:animator.set_bool("complete_attack",True)
            new_attack=lambda:animator.set_bool("complete_attack",False)

            ani["ComboAttack1"].get_frame_event(1) + hero.combo_attack_1 + complete_attack
            ani["ComboAttack2"].get_frame_event(1) + hero.combo_attack_2 + complete_attack
            ani["ComboAttack3"].get_frame_event(1) + hero.combo_attack_3 + complete_attack

            ani["ComboAttack1"].get_frame_event(0) + new_attack
            ani["ComboAttack2"].get_frame_event(0) + new_attack
            ani["ComboAttack3"].get_frame_event(0) + new_attack

            rigidbody.set_collider((40, 120, 40), (20, 0, 20))
            hero.set_brain(PlayerController())
            render.set_shadow_size((40, 40))
            return hero
