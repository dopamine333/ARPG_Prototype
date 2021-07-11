from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Scripts.CharacterBrain.CharacterBrain import CharacterBrain
from Scripts.Physics.RigidBody import RigidBody
from pygame import Vector2, Vector3
from Scripts.Graph.Image import Image
from Scripts.GameObject.Sprite.Sprite import Sprite


class Character(Sprite):
    def __init__(self, image: Image, position: Vector3, rigidbody: RigidBody, brain: CharacterBrain) -> None:
        super().__init__(image, position, rigidbody)

        self.brain = brain
        self.brain.set_character(self)
        self.force = 10
        self.speed = 1

    def move(self, direction: Vector2):
        direction.scale_to_length(self.speed)
        self.rigidbody.add_force(Vector3(direction.x, 0, direction.y))

    def jump(self):
        self.rigidbody.add_force(Vector3(0, self.force, 0))

    def attack(self):
        pass

    def start(self):
        super().start()
        self.brain.start()

    def update(self):
        super().update()
        self.brain.update()

    def end(self):
        super().end()
        self.brain.end()
