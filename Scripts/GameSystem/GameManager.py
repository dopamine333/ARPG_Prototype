from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pygame import Vector3
    from Scripts.Locals import CharacterID
from Scripts.GameSystem.PlayerSystem import PlayerSystem
from Scripts.GameSystem.EnemySystem import EnemySystem
from Scripts.Level.LevelSystem import LevelSystem
from Scripts.GameObject.Component import Component

class GameManager(Component):
    def __init__(self) -> None:
        super().__init__()
        self.levelsystem=LevelSystem(self)
        self.playersystem=PlayerSystem(self)
        self.enemysystem=EnemySystem(self)
    def start(self):
        self.levelsystem.start()
        self.playersystem.start()
        self.enemysystem.start()
    def update(self):
        self.levelsystem.update()
        self.playersystem.update()
        self.enemysystem.update()
    def end(self):
        self.levelsystem.end()
        self.playersystem.end()
        self.enemysystem.end()
    def generate_enemy(self,enemyID:CharacterID, startposition:Vector3):
        #TODO enemysystem.generate_enemy()
        pass