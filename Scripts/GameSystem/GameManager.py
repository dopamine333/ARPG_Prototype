from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pygame import Vector3
    from Scripts.Locals import CharacterID
    from Scripts.Level.Level import Level

from Scripts.Tools.Singleton import Singleton
from Scripts.GameSystem.PlayerSystem import PlayerSystem
from Scripts.GameSystem.EnemySystem import EnemySystem
from Scripts.Level.LevelSystem import LevelSystem


class GameManager(Singleton):
    def __init__(self) -> None:
        super().__init__()
        self.levelsystem = LevelSystem(self)
        self.playersystem = PlayerSystem(self)
        self.enemysystem = EnemySystem(self)
    
    def init(self):
        self.levelsystem.init()
        
    def start(self):
        self.levelsystem.start()
        self.playersystem.start()
        self.enemysystem.start()

    def update(self):
        self.levelsystem.update()
        self.playersystem.update()
        self.enemysystem.update()

    def release(self):
        self.levelsystem.release()

    def generate_enemy(self, enemies: list[tuple[CharacterID, Vector3]]):
        self.enemysystem.generate_enemy(enemies)

    def get_player(self):
        return self.playersystem.get_player()

    def get_spawnpoint(self):
        return self.levelsystem.current_level.current_savepoint.spawnpoint

    def choice_level(self, level_number: int):
        self.levelsystem.choice_level(level_number)

    def add_level(self, level: Level, level_number: int):
        self.levelsystem.add_level(level, level_number)
