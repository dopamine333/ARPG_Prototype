from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Scripts.Character.CharacterBrain.CharacterBrain import CharacterBrain
    from Scripts.Physics.Collision import Collision
    from Scripts.Attack.AttackParam import AttackParam
from Scripts.Attack.UnderAttackInterface import UnderAttackInterface
from Scripts.Tools.Buffer import Buffer
from Scripts.Locals import ForceMode
from Scripts.Physics.RigidBody import RigidBody

# TODO 衝刺


class Character(UnderAttackInterface):
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
        self.buffer = Buffer()
        self.invincible_time = 0.5
        self.max_hp = 10
        self.hp = self.max_hp
        self.is_dead = False

    def set_brain(self, brain: CharacterBrain):
        self.brain = brain
        self.brain.character = self

    def start(self):
        self.rigidbody = self.get_component(RigidBody)
        self.rigidbody.attach(self.on_collide)
        self.hp = self.max_hp
        self.brain.start()

    def update(self):
        if self.is_dead:
            return
        self.brain.update()
        self.buffer.update()

    def end(self):
        self.brain.end()

    def on_collide(self, collision: Collision):
        pass

    def under_attack(self, attack_param: AttackParam):
        if self.buffer.get("invincible"):
            return
        self.buffer.set("invincible", self.invincible_time)
        self.take_damage(attack_param)

    def take_damage(self, attack_param: AttackParam):
        self.rigidbody.add_force(attack_param.force, ForceMode.impulse)
        attack_param.set_defender(self)
        attack_param.show()
        self.hp -= attack_param.damage
        if self.hp <= 0:
            self.dead()

    def dead(self):
        self.is_dead = True
        self.destroy()
