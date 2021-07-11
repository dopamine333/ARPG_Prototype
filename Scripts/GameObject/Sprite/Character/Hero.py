
from Scripts.Physics.RigidBody import RigidBody
from Scripts.Graph.Image import Image
from Scripts.GameObject.Sprite.Character.Character import Character
from pygame import Vector2, Vector3


class Hero(Character):
    def start(self):
        super().start()
        self.force = 35
        self.speed = 2
        self.rigidbody.set_damp(0.92)
        self.rigidbody.set_horizontal_max_speed(6)

    def attack(self):
        print("hero attack!!!!")
