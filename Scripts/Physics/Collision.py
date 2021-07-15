from __future__ import annotations
from typing import Callable, TYPE_CHECKING
if TYPE_CHECKING:
    from Scripts.Physics.RigidBody import RigidBody
    from Scripts.Locals import Face


class Collision:
    """
    描述一個碰撞事件
    """

    def __init__(self, rigidbody: RigidBody, face: Face) -> None:
        self.rigidbody = rigidbody
        self.face = face
        if rigidbody:
            self.gameobject = rigidbody.gameobject
        else:
            self.gameobject = None
