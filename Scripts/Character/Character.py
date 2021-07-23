from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Scripts.Character.CharacterBrain.CharacterBrain import CharacterBrain
from Scripts.Physics.Collision import Collision
from Scripts.Locals import Face, ForceMode
from Scripts.Attack.AttackParam import AttackParam
from Scripts.Physics.RigidBody import RigidBody
from pygame import Vector2, Vector3
from Scripts.GameObject.Component import Component

# TODO 無敵時間
# TODO 跳躍冷卻
# TODO 衝刺


class Character(Component):
    '''
    場景上打來打去的角色

    有著攻擊，被攻擊，跳躍，移動，死亡等介面

    提供角色大腦(CharacterBrain)操控

    屬性:
        -jump_force: float = 10
        -speed: float = 1
        -face: Face = Face.right
        -max_hp: int = 10
        -brain: CharacterBrain
        +rigidbody: RigidBody

    要求組件:
        RigidBody
    '''

    def __init__(self) -> None:
        super().__init__()

        self.rigidbody: RigidBody = None
        self.brain: CharacterBrain = None

        self.jump_force = 10
        self.dash_force=10
        self.move_speed = 1
        self.face = Face.right
        self.max_hp = 10

        self.on_ground = False

    def set_brain(self, brain: CharacterBrain):
        self.brain = brain
        self.brain.character = self

    def start(self):
        self.rigidbody = self.get_component(RigidBody)
        self.rigidbody.attach(self.on_collide)
        self.hp = self.max_hp
        self.brain.start()

    def move(self, direction: Vector2):
        direction.scale_to_length(self.move_speed)
        self.rigidbody.add_force(
            Vector3(direction.x, 0, direction.y), ForceMode.force)

    def jump(self):
        if self.on_ground:
            self.rigidbody.add_force(
                Vector3(0, self.jump_force, 0), ForceMode.impulse)
            self.on_ground = False

    def attack(self):
        pass

    def dash(self):
        direction=self.rigidbody.velocity
        if direction.length_squared()<1:
            return
        direction.scale_to_length(self.dash_force)
        self.rigidbody.add_force(direction, ForceMode.impulse)

    def under_attack(self, attack_param: AttackParam):
        self.rigidbody.add_force(attack_param.force, ForceMode.impulse)
        attack_param.set_defender(self)
        attack_param.show()
        self.hp -= attack_param.damage
        if self.hp <= 0:
            self.dead()

    def update(self):
        self.brain.update()
        # 更新面向face
        acceleration = self.rigidbody.acceleration
        if acceleration.x > 0:
            self.face = Face.right
        elif acceleration.x < 0:
            self.face = Face.left

    def dead(self):
        self.destroy()

    def end(self):
        self.brain.end()

    def on_collide(self, collision: Collision):
        if collision.face == Face.down:
            self.on_ground = True
