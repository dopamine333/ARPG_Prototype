from __future__ import annotations
from time import time
from typing import TYPE_CHECKING

from pygame.time import Clock
if TYPE_CHECKING:
    from Scripts.Physics.RigidBody import RigidBody


from Scripts.EventManager.EventManager import EventManager
from Scripts.Physics.Collision import Collision
from Scripts.Locals import Face, InputEvent
from Scripts.Physics.Box import Box


class Physics:
    '''
    檢測剛體(RigidBody)間的物理碰撞

    並通知碰撞事件
    '''
    rigidbodies: list[RigidBody] = []
    elastic = True
    activity_box: Box = None
    lastframetime = time()
    deltatime = 0

    @staticmethod
    def init():
        # FIXME 測試用 切換是否為彈性碰撞
        EventManager.attach(InputEvent.change_collision_type,
                            Physics.change_collision_type)

    @staticmethod
    def set_clock(clock: Clock):
        Physics.clock = clock

    @staticmethod
    def update():
        if len(Physics.rigidbodies) != 0:
            Physics.deltatime = Physics.clock.get_time()*0.001

    @staticmethod
    def get_deltatime():
        return Physics.deltatime

    @staticmethod
    def change_collision_type():
        Physics.elastic = not Physics.elastic
        print(Physics.elastic)

    @staticmethod
    def set_activity_box(activity_box: Box):
        Physics.activity_box = activity_box

    @staticmethod
    def check(rigidbody: RigidBody):
        '''
        每當有剛體(RigidBody)移動時，

        呼叫此方法，檢查是否碰撞其他剛體，
        '''
        if Physics.activity_box:
            Physics.check_activity_box(rigidbody)
            pass

        for other_rigidbody in Physics.rigidbodies:
            if rigidbody == other_rigidbody:
                continue
            Physics.collide(rigidbody, other_rigidbody)

    @staticmethod
    def overlap_box(box: Box) -> list[RigidBody]:
        '''回傳所有與輸入的箱子碰撞的剛體(RigidBody)'''
        a = box
        collided_rigidbody = []
        for b in Physics.rigidbodies:
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

    @staticmethod
    def check_activity_box(rigidbody: RigidBody):
        '''將剛體限制在活動範圍裡(activity_box)'''
        if rigidbody.get_surface(Face.right) > (activity_box_surface := Physics.activity_box.get_surface(Face.right)):
            rigidbody.set_surface(Face.right, activity_box_surface)
            rigidbody.velocity.x = 0
        elif rigidbody.get_surface(Face.left) < (activity_box_surface := Physics.activity_box.get_surface(Face.left)):
            rigidbody.set_surface(Face.left, activity_box_surface)
            rigidbody.velocity.x = 0
        if rigidbody.get_surface(Face.front) > (activity_box_surface := Physics.activity_box.get_surface(Face.front)):
            rigidbody.set_surface(Face.front, activity_box_surface)
            rigidbody.velocity.z = 0
        elif rigidbody.get_surface(Face.back) < (activity_box_surface := Physics.activity_box.get_surface(Face.back)):
            rigidbody.set_surface(Face.back, activity_box_surface)
            rigidbody.velocity.z = 0
        if rigidbody.get_surface(Face.up) > (activity_box_surface := Physics.activity_box.get_surface(Face.up)):
            rigidbody.set_surface(Face.up, activity_box_surface)
            rigidbody.velocity.y = 0
        elif rigidbody.get_surface(Face.down) < (activity_box_surface := Physics.activity_box.get_surface(Face.down)):
            rigidbody.set_surface(Face.down, activity_box_surface)
            rigidbody.velocity.y = 0
            rigidbody.on_collide(Collision(None, Face.down))

    @staticmethod
    def collide(a: RigidBody, b: RigidBody):
        '''檢測碰撞、應用碰撞效果、通知剛體碰撞事件'''
        # 是否碰撞
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
            # 尋找碰撞到哪一面(兩剛體最近的面)
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
                a.on_collide(Collision(b, Face.right))
                b.on_collide(Collision(a, Face.left))
                # 彈性碰撞
                if Physics.elastic:
                    a.velocity.x, b.velocity.x = b.velocity.x, a.velocity.x
                # 非彈性碰撞
                else:
                    average_velocity = (a.velocity.x+b.velocity.x)/2
                    a.velocity.x = average_velocity
                    b.velocity.x = average_velocity
            elif min_distance == b_rigth_a_left:
                a.set_surface(Face.left, b_rigth)
                a.on_collide(Collision(b, Face.left))
                b.on_collide(Collision(a, Face.right))
                # 彈性碰撞
                if Physics.elastic:
                    a.velocity.x, b.velocity.x = b.velocity.x, a.velocity.x
                # 非彈性碰撞
                else:
                    average_velocity = (a.velocity.x+b.velocity.x)/2
                    a.velocity.x = average_velocity
                    b.velocity.x = average_velocity
            elif min_distance == a_front_b_back:
                a.set_surface(Face.front, b_back)
                a.on_collide(Collision(b, Face.front))
                b.on_collide(Collision(a, Face.back))
                # 彈性碰撞
                if Physics.elastic:
                    a.velocity.z, b.velocity.z = b.velocity.z, a.velocity.z
                # 非彈性碰撞
                else:
                    average_velocity = (a.velocity.z+b.velocity.z)/2
                    a.velocity.z = average_velocity
                    b.velocity.z = average_velocity
            elif min_distance == b_front_a_back:
                a.set_surface(Face.back, b_front)
                a.on_collide(Collision(b, Face.back))
                b.on_collide(Collision(a, Face.front))
                # 彈性碰撞
                if Physics.elastic:
                    a.velocity.z, b.velocity.z = b.velocity.z, a.velocity.z
                # 非彈性碰撞
                else:
                    average_velocity = (a.velocity.z+b.velocity.z)/2
                    a.velocity.z = average_velocity
                    b.velocity.z = average_velocity

            elif min_distance == a_up_b_down:
                a.set_surface(Face.up, b_down)
                a.on_collide(Collision(b, Face.up))
                b.on_collide(Collision(a, Face.down))
                # 彈性碰撞
                if Physics.elastic:
                    a.velocity.y, b.velocity.y = b.velocity.y, a.velocity.y
                # 非彈性碰撞
                else:
                    average_velocity = (a.velocity.y+b.velocity.y)/2
                    a.velocity.y = average_velocity
                    b.velocity.y = average_velocity
            elif min_distance == b_up_a_down:
                a.set_surface(Face.down, b_up)
                a.on_collide(Collision(b, Face.down))
                b.on_collide(Collision(a, Face.up))
                # 彈性碰撞
                if Physics.elastic:
                    a.velocity.y, b.velocity.y = b.velocity.y, a.velocity.y
                # 非彈性碰撞
                else:
                    average_velocity = (a.velocity.y+b.velocity.y)/2
                    a.velocity.y = average_velocity
                    b.velocity.y = average_velocity

    @staticmethod
    def attach(rigidbody: RigidBody):
        '''註冊剛體(RigidBody)'''
        Physics.rigidbodies.append(rigidbody)

    @staticmethod
    def detach(rigidbody: RigidBody):
        '''取消註冊剛體(RigidBody)'''
        if rigidbody in Physics.rigidbodies:
            Physics.rigidbodies.remove(rigidbody)
