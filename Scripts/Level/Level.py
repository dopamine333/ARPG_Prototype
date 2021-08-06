from __future__ import annotations
from random import random
from typing import TYPE_CHECKING

from pygame.draw import circle
if TYPE_CHECKING:
    from Scripts.Level.LevelSystem import LevelSystem

from pygame import Surface, Vector3, mouse
from pygame.image import load
from pygame.transform import scale
from Scripts.Graphic.Image import Image
from Scripts.Locals import CharacterID, Tag
from Scripts.Physics.Physics import Physics
from Scripts.Graphic.RenderManager import RenderManager
from Scripts.Level.CheckPoint import Checkpoint
from Scripts.Level.SavePoint import SavePoint


class Level:
    def __init__(self) -> None:

        self.savepoints: list[SavePoint] = []
        self.current_checkpoint: Checkpoint = None
        self.current_savepoint: SavePoint = None

        self.default_savepoint: SavePoint = None

        self.levelsystem: LevelSystem = None

    def set_levelsystem(self, levelsystem: LevelSystem):
        self.levelsystem = levelsystem
    
    def start(self):
        self.bg_sketch = Surface((14000, 200))
        self.bg_sketch.fill((204, 154, 15))
        for _ in range(1000):
            circle(self.bg_sketch,(random()*255,random()*20,random()*255),(random()*14000,random()*200),random()*30+5)

        self.current_checkpoint.detect()
        self.current_checkpoint.apply_physics_activity_box(self.current_checkpoint.physics_activity_box)
        self.current_checkpoint.apply_render_activity_rect(self.current_checkpoint.render_activity_rect)

        self.current_savepoint = self.default_savepoint

    def update(self):
        self.current_checkpoint.update()
        # self.current_savepoint.update()
        # FIXME 測試用畫背景
        RenderManager.camera.draw_background(
            Image(self.bg_sketch, (0, 0)), Vector3(0, 0, 400))

    def finish_checkpoint(self):
        print("level:finish_checkpoint")
        self.current_checkpoint = self.current_checkpoint.next_checkpoint

    def finish_level(self):
        # TODO 結束關卡通知
        print("level:finish_level")
    def generate_enemy(self, enemies: list[tuple[CharacterID, Vector3]]):
        self.levelsystem.generate_enemy(enemies)
    # region add checkpoints and savepoints

    def add_checkpoints(self, *checkpoints: Checkpoint):
        for checkpoint in checkpoints:
            self.add_checkpoint(checkpoint)

    def add_checkpoint(self, checkpoint: Checkpoint):
        checkpoint.set_level(self)
        if self.current_checkpoint:
            self.current_checkpoint.add_checkpoint(checkpoint)
        else:
            self.current_checkpoint=checkpoint
        

    def add_savepoints(self, *savepoints: SavePoint):
        self.savepoints.extend(savepoints)

    def add_savepoint(self, savepoint: SavePoint):
        self.savepoints.append(savepoint)
        self.default_savepoint

    def set_default_savepoint(self, default_savepoint: SavePoint):
        self.default_savepoint = default_savepoint
    # endregion
