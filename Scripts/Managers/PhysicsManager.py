from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Scripts.Physics.RigidBody import RigidBody
    
from Scripts.Locals import Face
from Scripts.Tools.Singleton import Singleton


class PhysicsManager(Singleton):
    def __init__(self) -> None:
        self.rigidbodies: list[RigidBody] = []
    
    def update(self):
        for rigidbody in self.rigidbodies:
            if rigidbody.get_surface(Face.down)<0:
                rigidbody.set_surface(Face.down,0)
                rigidbody.velocity.y=0

    def attach(self, rigidbody: RigidBody):
        self.rigidbodies.append(rigidbody)

    def detach(self, rigidbody: RigidBody):
        if rigidbody in self.rigidbodies:
            self.rigidbodies.remove(rigidbody)
