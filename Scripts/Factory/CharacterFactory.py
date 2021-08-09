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
        acts = ["Dead", "Idle", "Jump", "Run"]
        for act in acts:
            clip = []
            for i in range(1, 16):
                clip.append(Image(
                    scale(load(f"Arts\Character\hero\{act} ({i}).png"), (150, 150)).convert_alpha(), (30, 140)))
            self.hero_animation_clips[act] = clip
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
            animations: dict[str, Animation] = {}
            for act, clip in self.hero_animation_clips.items():
                animations[act] = Animation()
                animations[act].set_clip(clip)
                animations[act].set_speed(0.5)
            animations["Dead"].set_speed(0.1)
            gameobject = GameObject()
            hero = gameobject.add_component(Hero)
            rigidbody = gameobject.add_component(RigidBody)
            render = gameobject.add_component(SpriteRender)
            animator = gameobject.add_component(Animator)
            animator.add_animations(*animations.values())
            animator.set_default_animation(animations["Idle"])
            animations["Dead"].attach(14, gameobject.destroy)
            # TODO 註冊動畫事件應該在Character裡 還是在工廠裡
            animations["Run"].attach(0, hero.play_move_VFX_and_SFX)
            animations["Run"].attach(8, hero.play_move_VFX_and_SFX)
            animator.add_bool("running", "on_ground", "dead")
            animations["Idle"].set_play_mode(PlayMode.loop)
            animations["Jump"].set_play_mode(PlayMode.once)
            animations["Run"].set_play_mode(PlayMode.loop)
            animations["Dead"].set_play_mode(PlayMode.once)
            animations["Idle"].add_transition(
                animations["Run"], False, ("running", True))
            animations["Idle"].add_transition(
                animations["Jump"], False, ("on_ground", False))
            animations["Jump"].add_transition(
                animations["Idle"], False, ("on_ground", True))
            animations["Run"].add_transition(
                animations["Idle"], False, ("running", False))
            animations["Run"].add_transition(
                animations["Jump"], False, ("on_ground", False))
            animations["Idle"].add_transition(
                animations["Dead"], False, ("dead", True))
            animations["Jump"].add_transition(
                animations["Dead"], False, ("dead", True))
            animations["Run"].add_transition(
                animations["Dead"], False, ("dead", True))

            rigidbody.set_collider((40, 120, 40), (20, 0, 20))
            hero.set_brain(PlayerController())
            render.set_shadow_size((40, 40))
            return hero
