from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Scripts.Level.Level import Level
from Scripts.Level.CheckPoint import Checkpoint
from Scripts.Locals import OnLevelGameObjectID
from Scripts.Factory.FactoryManager import FactoryManager
from Scripts.Level.GoldSword import GoldSword
from pygame import Vector3


class SavePoint:
    def __init__(self) -> None:
        self.spawnpoint = Vector3()
        self.goldsword_position = Vector3()
        self.goldsword: GoldSword = None

        self.current_checkpoint: Checkpoint = None

        self.level: Level = None

    def init(self):
        factory = FactoryManager.Instance().get_onlevelgameobjectfactory()
        self.goldsword = factory.create(OnLevelGameObjectID.goldsword)
        self.goldsword.set_savepoint(self)
        self.goldsword.gameobject.set_position(self.goldsword_position)
        self.goldsword.gameobject.instantiate()

    def trigger(self):
        self.goldsword.trigger()
        self.current_checkpoint = self.level.get_current_checkpoint()
        self.level.trigger_savepoint(self)

    def get_current_checkpoint(self):
        return self.current_checkpoint

    def set_level(self, level: Level):
        self.level = level

    def get_spawnpoint(self):
        return self.spawnpoint

    def set_spawnpoint(self, spawnpoint: Vector3):
        self.spawnpoint = spawnpoint

    def set_goldsword_position(self, goldsword_position: Vector3):
        self.goldsword_position = goldsword_position
