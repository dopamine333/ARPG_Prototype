from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Scripts.Level.Level import Level
from Scripts.Camera.CameraController import CameraController
from Scripts.EventManager.EventManager import EventManager
from Scripts.Physics.Physics import Physics
from Scripts.Graphic.Image import Image
from Scripts.Graphic.RenderManager import RenderManager
from Scripts.Locals import CharacterID, Face, GameEvent, Tag
from pygame import Rect, Surface, Vector3
from Scripts.Physics.Box import Box


class Checkpoint:
    def __init__(self) -> None:
        self.level: Level = None
        self.next_checkpoint: Checkpoint = None

        self.trigger_box: Box = None
        self.physics_activity_box: Box = None
        self.render_activity_rect: Rect = None
        self.enemies: list[tuple[CharacterID, Vector3]] = []

        self.trigger_box_sketch: Surface = None
        self.trigger_box_sketch_position = Vector3()

        self.finish_event: GameEvent = None

        self.is_detecting = False
        #self.is_triggered = False

    def detect(self):
        '''開始偵測玩家'''
        self.is_detecting = True

    def resume(self):
        self.stop_detect()

        # if self.is_triggered:

        EventManager.detach(self.finish_event, self.finish)

    def finish(self):
        '''完成一個檢查點'''
        # 解除註冊使該檢查點結束的事件
        EventManager.detach(self.finish_event, self.finish)
        # 如果是最後檢查點 通知關卡結束
        if self.is_final_checkpoint():
            self.level.finish_level()
            return
        # 通知關卡切換致下個檢查點
        self.level.finish_checkpoint()
        # 將相機與物理限制在上個檢查點與當前檢查點之內
        self.apply_self_and_next_activity_range()
        # 下個檢查點開始偵測
        self.next_checkpoint.detect()

    def apply_self_and_next_activity_range(self):
        self.apply_physics_activity_box(self.physics_activity_box.union(
            self.next_checkpoint.physics_activity_box))
        self.apply_render_activity_rect(self.render_activity_rect.union(
            self.next_checkpoint.render_activity_rect))

    def apply_self_activity_range(self):
        self.apply_render_activity_rect(self.render_activity_rect)
        self.apply_physics_activity_box(self.physics_activity_box)

    def update(self):
        # 檢測玩家是否觸發檢查點
        if self.is_detecting:
            for rigidbody in Physics.overlap_box(self.trigger_box):
                if rigidbody.compare_tag(Tag.player):
                    self.stop_detect()
                    self.trigger()
                    break

            # TODO 明顯的觸發檢查點位子提示
            RenderManager.camera.draw(
                Image(self.trigger_box_sketch, (0, 0)), self.trigger_box_sketch_position)

    def stop_detect(self):
        self.is_detecting = False

    def trigger(self):
        '''玩家進入觸發檢查點'''
        #self.is_triggered = True
        self.level.trigger_checkpoint()
        # 生成怪物
        self.generate_enemy(self.enemies)
        # 將相機與物理限制在當前檢查點之內
        self.apply_self_activity_range()
        # 註冊使該檢查點結束的事件
        EventManager.attach(self.finish_event, self.finish)

    def apply_render_activity_rect(self, render_activity_rect: Rect):
        RenderManager.camera.get_component(
            CameraController).set_activity_rect(render_activity_rect)

    def apply_physics_activity_box(self, physics_activity_box: Box):
        Physics.set_activity_box(physics_activity_box)

    def generate_enemy(self, enemies: list[tuple[CharacterID, Vector3]]):
        self.level.generate_enemy(enemies)

    def set_level(self, level: Level):
        self.level = level

    def set_next_checkpoint(self, next_checkpoint: Checkpoint):
        self.next_checkpoint = next_checkpoint

    def set_trigger_box(self, trigger_box: Box):
        self.trigger_box = trigger_box

    def set_physics_activity_box(self, physics_activity_box: Box):
        self.physics_activity_box = physics_activity_box

    def set_render_activity_rect(self, render_activity_rect: Rect):
        self.render_activity_rect = render_activity_rect

    def set_trigger_box_sketch(self, trigger_box_sketch: Surface):
        self.trigger_box_sketch = trigger_box_sketch

    def set_trigger_box_sketch_position(self, trigger_box_sketch_position: Vector3):
        self.trigger_box_sketch_position = trigger_box_sketch_position

    def set_finish_event(self, finish_event: GameEvent):
        self.finish_event = finish_event

    def add_enemies(self, *enemies: tuple[CharacterID, Vector3]):
        self.enemies.extend(enemies)

    def add_enemy(self, enemy: tuple[CharacterID, Vector3]):
        self.enemies.append(enemy)

    def add_checkpoint(self, checkpoint: Checkpoint):
        '''在最尾端加入一個新的檢察點'''
        if self.next_checkpoint:
            self.next_checkpoint.add_checkpoint(checkpoint)
        else:
            self.next_checkpoint = checkpoint

    def get_final_checkpoint(self):
        '''得到最後一個檢查點'''
        return self \
            if self.is_final_checkpoint()\
            else self.next_checkpoint.get_final_checkpoint()

    def is_final_checkpoint(self):
        '''是否是最後一個檢查點'''
        return not self.next_checkpoint
