from __future__ import annotations
from typing import TYPE_CHECKING
from pygame import Surface, Vector3, mouse
if TYPE_CHECKING:
    from Scripts.Level.LevelSystem import LevelSystem

from pygame.image import load
from pygame.transform import scale
from Scripts.Graphic.Image import Image
from Scripts.Locals import Tag
from Scripts.Physics.Physics import Physics
from Scripts.Graphic.RenderManager import RenderManager
from Scripts.Level.CheckPoint import Checkpoint
from Scripts.Level.SavePoint import SavePoint


class Level:
    def __init__(self) -> None:
        self.checkpoints: list[Checkpoint] = []
        self.savepoints: list[SavePoint] = []
        self.current_checkpoint: Checkpoint = None
        self.current_savepoint: SavePoint = None
        self.current_checkpoint_number = 1
        self.default_savepoint: SavePoint = None

        self.levelsystem: LevelSystem = None

    def set_levelsystem(self, levelsystem: LevelSystem):
        self.levelsystem = levelsystem

    def get_current_checkpoint(self):
        if self.current_checkpoint_number > len(self.checkpoints):
            raise Exception("unknow level!!")
        return self.checkpoints[self.current_checkpoint_number-1]

    def start(self):
        
        self.bg_sketch=Surface((2000,200))
        self.bg_sketch.fill((204,154,15))
        self.checkpoint_range_sketch=Surface((10,200))
        self.checkpoint_range_sketch.fill((208,37,37))

        self.current_checkpoint = self.get_current_checkpoint()
        self.current_checkpoint.detecting=True

        self.current_savepoint = self.default_savepoint

    def trigger_current_checkpoint(self):
        '''玩家進入觸發檢查點'''
        #生成怪物
        self.levelsystem.gamemanager.generate_enemy(self.current_checkpoint.enemies)
        #將相機與物理限制在當前檢查點之內
        print(RenderManager.camera.view_rect)
        RenderManager.camera.set_activity_rect(
            self.current_checkpoint.render_activity_rect)
        print(RenderManager.camera.view_rect)
        Physics.set_activity_box(self.current_checkpoint.physics_activity_box)

    def finish_current_checkpoint(self):
        '''完成一個檢查點'''
        #是否是最後一個檢查點
        if self.current_checkpoint_number >= len(self.checkpoints):
            self.finish_level()
            return
        #當前檢查點加一
        self.current_checkpoint_number += 1
        next_checkpoint = self.get_current_checkpoint()
        #將相機與物理限制在上個檢查點與當前檢查點之內
        union_render_activity_rect = self.current_checkpoint.render_activity_rect.union(
            next_checkpoint.render_activity_rect)
        union_physics_activity_box = self.current_checkpoint.physics_activity_box.union(
            next_checkpoint.physics_activity_box)
        RenderManager.camera.set_activity_rect(union_render_activity_rect)
        Physics.set_activity_box(union_physics_activity_box)
        self.current_checkpoint = next_checkpoint
        #開始檢測玩家是否觸發檢查點
        self.current_checkpoint.detecting=True
    def update(self):
        #檢測玩家是否觸發檢查點
        if self.current_checkpoint.detecting:
            for rigidbody in Physics.overlap_box(self.current_checkpoint.trigger_box):
                if rigidbody.compare_tag(Tag.player):
                    self.current_checkpoint.detecting = False
                    self.trigger_current_checkpoint()
                    break
            
            RenderManager.camera.draw(Image(self.checkpoint_range_sketch,(0,0)),Vector3(700,0,400))
        #FIXME 測試用畫背景
        x,y=mouse.get_pos()
        RenderManager.camera.draw(Image(self.bg_sketch,(0,0)),Vector3(0,0,400))
    
    def finish_level(self):
        #TODO 結束關卡通知
        print("finish_level")


    #region add checkpoints and savepoints
    def add_checkpoints(self, *checkpoints: Checkpoint):
        self.checkpoints.extend(checkpoints)

    def add_checkpoint(self, checkpoint: Checkpoint):
        self.checkpoints.append(checkpoint)

    def insert_checkpoint(self, checkpoint: Checkpoint, checkpoint_number: int):
        self.checkpoints.insert(checkpoint_number-1, checkpoint)

    def add_savepoints(self, *savepoints: SavePoint):
        self.savepoints.extend(savepoints)

    def add_savepoint(self, savepoint: SavePoint):
        self.savepoints.append(savepoint)
        self.default_savepoint
    def set_default_savepoint(self,default_savepoint:SavePoint):
        self.default_savepoint=default_savepoint
    #endregion