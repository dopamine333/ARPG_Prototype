from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Scripts.CharacterBrain.CharacterBrain import CharacterBrain
from Scripts.Locals import Face, GameEvent
from Scripts.Attack.AttackParam import AttackParam
from Scripts.Physics.RigidBody import RigidBody
from pygame import Vector2, Vector3
from Scripts.Graph.Image import Image
from Scripts.GameObject.Sprite.Sprite import Sprite
from Scripts.Managers.EventManager import EventManager

class Character(Sprite):
    def __init__(self, image: Image, position: Vector3, rigidbody: RigidBody, brain: CharacterBrain) -> None:
        super().__init__(image, position, rigidbody)

        self.brain = brain
        self.brain.set_character(self)
        self.force = 10
        self.speed = 1
        self.face=Face.right

        self.max_hp=10

    def move(self, direction: Vector2):
        direction.scale_to_length(self.speed)
        self.rigidbody.add_force(Vector3(direction.x, 0, direction.y))

    def jump(self):
        self.rigidbody.add_force(Vector3(0, self.force, 0))

    def attack(self):
        pass
    def under_attack(self, attack_param: AttackParam):
        self.rigidbody.add_force(attack_param.force)
        attack_param.set_defender(self)
        attack_param.show()
        self.hp-=attack_param.damage
        if self.hp<=0:
            self.dead()
    def start(self):
        super().start()
        self.hp=self.max_hp
        self.brain.start()

    def update(self):
        super().update()
        self.brain.update()
        acceleration=self.rigidbody.acceleration
        if acceleration.x>acceleration.z and acceleration.x>-acceleration.z:
            self.face=Face.right
        elif acceleration.x<acceleration.z and acceleration.x<-acceleration.z:
            self.face=Face.left

    def dead(self):
        self.end()
        EventManager.notify(GameEvent.remove_gameobject,self)
    def end(self):
        super().end()
        self.brain.end()
