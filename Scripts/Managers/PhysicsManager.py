from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Scripts.Physics.RigidBody import RigidBody

from Scripts.Physics.Collider import Collider
from Scripts.Physics.Collision import Collision
from Scripts.Locals import Face
from Scripts.Tools.Singleton import Singleton
from Scripts.Physics.Box import Box

class PhysicsManager(Singleton):
    def __init__(self) -> None:
        self.rigidbodies: list[RigidBody] = []
        self.elastic = True
        self.activity_box: Collider = None
        
    def check(self, rigidbody: RigidBody):

        for other_rigidbody in self.rigidbodies:
            if rigidbody == other_rigidbody:
                continue
            if self.activity_box:
                self.check_activity_box(rigidbody)
                pass
            self.collide(rigidbody, other_rigidbody)

    def overlap_box(self,a:Box)-> list[RigidBody]:
        collided_rigidbody=[]
        for b in self.rigidbodies:
            a_rigth = a.get_surface(Face.right)
            a_left = a.get_surface(Face.left)
            b_rigth = b.get_surface(Face.right)
            b_left = b.get_surface(Face.left)
            if a_rigth >= b_left and b_rigth >= a_left:
                a_front = a.get_surface(Face.front)
                a_back = a.get_surface(Face.back)
                b_front = b.get_surface(Face.front)
                b_back = b.get_surface(Face.back)
                if a_front >= b_back and b_front >= a_back:
                    a_up = a.get_surface(Face.up)
                    a_down = a.get_surface(Face.down)
                    b_up = b.get_surface(Face.up)
                    b_down = b.get_surface(Face.down)
                    if a_up >= b_down and b_up >= a_down:
                        collided_rigidbody.append(b)
        return collided_rigidbody
    def set_activity_box(self, box: Box):
        self.activity_box = box

    def check_activity_box(self, rigidbody: RigidBody):
        if rigidbody.get_surface(Face.right) > (activity_box_surface := self.activity_box.get_surface(Face.right)):
            rigidbody.set_surface(Face.right, activity_box_surface)
            rigidbody.velocity.x = 0
        if rigidbody.get_surface(Face.up) > (activity_box_surface := self.activity_box.get_surface(Face.up)):
            rigidbody.set_surface(Face.up, activity_box_surface)
            rigidbody.velocity.y = 0
        if rigidbody.get_surface(Face.front) > (activity_box_surface := self.activity_box.get_surface(Face.front)):
            rigidbody.set_surface(Face.front, activity_box_surface)
            rigidbody.velocity.z = 0
        if rigidbody.get_surface(Face.left) < (activity_box_surface := self.activity_box.get_surface(Face.left)):
            rigidbody.set_surface(Face.left, activity_box_surface)
            rigidbody.velocity.x = 0
        if rigidbody.get_surface(Face.down) < (activity_box_surface := self.activity_box.get_surface(Face.down)):
            rigidbody.set_surface(Face.down, activity_box_surface)
            rigidbody.velocity.y = 0
        if rigidbody.get_surface(Face.back) < (activity_box_surface := self.activity_box.get_surface(Face.back)):
            rigidbody.set_surface(Face.back, activity_box_surface)
            rigidbody.velocity.z = 0

    def collide(self, a: RigidBody, b: RigidBody):

        collide = False
        a_rigth = a.get_surface(Face.right)
        a_left = a.get_surface(Face.left)
        b_rigth = b.get_surface(Face.right)
        b_left = b.get_surface(Face.left)
        if a_rigth >= b_left and b_rigth >= a_left:
            a_front = a.get_surface(Face.front)
            a_back = a.get_surface(Face.back)
            b_front = b.get_surface(Face.front)
            b_back = b.get_surface(Face.back)
            if a_front >= b_back and b_front >= a_back:
                a_up = a.get_surface(Face.up)
                a_down = a.get_surface(Face.down)
                b_up = b.get_surface(Face.up)
                b_down = b.get_surface(Face.down)
                if a_up >= b_down and b_up >= a_down:
                    collide = True
        if collide:
            a_rigth_b_left = a_rigth-b_left
            b_rigth_a_left = b_rigth-a_left
            a_front_b_back = a_front-b_back
            b_front_a_back = b_front-a_back
            a_up_b_down = a_up-b_down
            b_up_a_down = b_up-a_down

            min_distance = min(a_rigth_b_left,
                               b_rigth_a_left,
                               a_front_b_back,
                               b_front_a_back,
                               a_up_b_down,
                               b_up_a_down)
            if min_distance == a_rigth_b_left:
                a.set_surface(Face.right, b_left)
                a.collide(Collision(b, Face.right))
                b.collide(Collision(a, Face.left))
                # 彈性碰撞
                if self.elastic:
                    a.velocity.x, b.velocity.x = b.velocity.x, a.velocity.x
                # 非彈性碰撞
                else:
                    average_velocity = (a.velocity.x+b.velocity.x)/2
                    a.velocity.x = average_velocity
                    b.velocity.x = average_velocity
            elif min_distance == b_rigth_a_left:
                a.set_surface(Face.left, b_rigth)
                a.collide(Collision(b, Face.left))
                b.collide(Collision(a, Face.right))
                # 彈性碰撞
                if self.elastic:
                    a.velocity.x, b.velocity.x = b.velocity.x, a.velocity.x
                # 非彈性碰撞
                else:
                    average_velocity = (a.velocity.x+b.velocity.x)/2
                    a.velocity.x = average_velocity
                    b.velocity.x = average_velocity
            elif min_distance == a_front_b_back:
                a.set_surface(Face.front, b_back)
                a.collide(Collision(b, Face.front))
                b.collide(Collision(a, Face.back))
                # 彈性碰撞
                if self.elastic:
                    a.velocity.z, b.velocity.z = b.velocity.z, a.velocity.z
                # 非彈性碰撞
                else:
                    average_velocity = (a.velocity.z+b.velocity.z)/2
                    a.velocity.z = average_velocity
                    b.velocity.z = average_velocity
            elif min_distance == b_front_a_back:
                a.set_surface(Face.back, b_front)
                a.collide(Collision(b, Face.back))
                b.collide(Collision(a, Face.front))
                # 彈性碰撞
                if self.elastic:
                    a.velocity.z, b.velocity.z = b.velocity.z, a.velocity.z
                # 非彈性碰撞
                else:
                    average_velocity = (a.velocity.z+b.velocity.z)/2
                    a.velocity.z = average_velocity
                    b.velocity.z = average_velocity

            elif min_distance == a_up_b_down:
                a.set_surface(Face.up, b_down)
                a.collide(Collision(b, Face.up))
                b.collide(Collision(a, Face.down))
                # 彈性碰撞
                if self.elastic:
                    a.velocity.y, b.velocity.y = b.velocity.y, a.velocity.y
                # 非彈性碰撞
                else:
                    average_velocity = (a.velocity.y+b.velocity.y)/2
                    a.velocity.y = average_velocity
                    b.velocity.y = average_velocity
            elif min_distance == b_up_a_down:
                a.set_surface(Face.down, b_up)
                a.collide(Collision(b, Face.down))
                b.collide(Collision(a, Face.up))
                # 彈性碰撞
                if self.elastic:
                    a.velocity.y, b.velocity.y = b.velocity.y, a.velocity.y
                # 非彈性碰撞
                else:
                    average_velocity = (a.velocity.y+b.velocity.y)/2
                    a.velocity.y = average_velocity
                    b.velocity.y = average_velocity

    def attach(self, rigidbody: RigidBody):
        self.rigidbodies.append(rigidbody)

    def detach(self, rigidbody: RigidBody):
        if rigidbody in self.rigidbodies:
            self.rigidbodies.remove(rigidbody)
