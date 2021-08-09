from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Scripts.Level.LevelSystem import LevelSystem
from Scripts.VFXManager.VFXManager import VFXManager
from random import random
from Scripts.EventManager.EventManager import EventManager
from pygame.draw import circle

from pygame import Surface, Vector3, mouse
from pygame.image import load
from pygame.transform import scale
from Scripts.Graphic.Image import Image
from Scripts.Locals import CharacterID, GameEvent, Tag, VFXID
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

    def start_level(self):
        self.bg_sketch = Surface((14000, 200))
        self.bg_sketch.fill((204, 154, 15))
        for _ in range(1000):
            circle(self.bg_sketch, (random()*30+200, random()*30+150,
                   random()*30+10), (random()*14000, random()*200), random()*30+5)

        self.current_checkpoint.detect()
        self.current_checkpoint.apply_self_activity_range()

        for savepoint in self.savepoints:
            savepoint.start()
        self.default_savepoint.trigger()

        EventManager.attach(GameEvent.player_dead,
                            self.back_to_current_savepoint)

    def back_to_current_savepoint(self):
        self.current_checkpoint.resume()
        self.current_checkpoint = self.current_savepoint.get_current_checkpoint()

        self.current_checkpoint.detect()
        self.current_checkpoint.apply_self_activity_range()

    def update(self):
        self.current_checkpoint.update()
        # self.current_savepoint.update()
        # FIXME 測試用畫背景
        RenderManager.camera.draw_background(
            Image(self.bg_sketch, (0, 0)), Vector3(0, 0, 400))

    def finish_checkpoint(self):
        # FIXME 完成檢查點視覺提示
        position = self.levelsystem.gamemanager.get_player().position.xyz
        position.y += 200
        VFXManager.Instance().play(VFXID.finish_checkpoint, position)
        self.current_checkpoint = self.current_checkpoint.next_checkpoint

    def finish_level(self):
        # TODO 結束關卡通知
        position = self.levelsystem.gamemanager.get_player().position.xyz
        position.y += 200
        VFXManager.Instance().play(VFXID.finish_level, position)
        EventManager.detach(GameEvent.player_dead,
                            self.back_to_current_savepoint)

    def trigger_checkpoint(self):
        # FIXME 進入檢查點視覺提示
        position = self.current_checkpoint.trigger_box_sketch_position.xyz
        position.y += 200
        VFXManager.Instance().play(VFXID.trigger_checkpoint, position)

    def trigger_savepoint(self, savepoint: SavePoint):
        # FIXME 觸發存檔點視覺提示
        position = savepoint.goldsword.position.xyz
        position.y += 200
        VFXManager.Instance().play(VFXID.trigger_savepoint, position)
        self.current_savepoint = savepoint

    def generate_enemy(self, enemies: list[tuple[CharacterID, Vector3]]):
        self.levelsystem.generate_enemy(enemies)

    def get_current_checkpoint(self):
        return self.current_checkpoint
    # region add checkpoints and savepoints

    def add_checkpoints(self, *checkpoints: Checkpoint):
        for checkpoint in checkpoints:
            self.add_checkpoint(checkpoint)

    def add_checkpoint(self, checkpoint: Checkpoint):
        checkpoint.set_level(self)
        if self.current_checkpoint:
            self.current_checkpoint.add_checkpoint(checkpoint)
        else:
            self.current_checkpoint = checkpoint

    def add_savepoints(self, *savepoints: SavePoint):
        for savepoint in savepoints:
            self.add_savepoint(savepoint)

    def add_savepoint(self, savepoint: SavePoint):
        savepoint.set_level(self)
        self.savepoints.append(savepoint)

    def set_default_savepoint(self, default_savepoint: SavePoint):
        self.default_savepoint = default_savepoint
    # endregion
