from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Scripts.GameSystem.GameManager import GameManager

from pygame import Vector3
from Scripts.Locals import CharacterID
from Scripts.Level.Level import Level
from Scripts.GameSystem.GameSystem import GameSystem


class LevelSystem(GameSystem):
    def __init__(self, gamemanager: GameManager) -> None:
        super().__init__(gamemanager)
        self.current_level_number = 1
        self.current_level: Level = None
        self.levels: list[Level] = []

    def start(self):
        if self.current_level_number > len(self.levels):
            raise Exception("unknow level!!")
        self.current_level = self.levels[self.current_level_number-1]
        self.current_level.start()

    def update(self):
        self.current_level.update()

    def get_spawnpoint(self):
        return self.current_level.current_savepoint.spawnpoint
        
    def generate_enemy(self, enemies: list[tuple[CharacterID, Vector3]]):
        self.gamemanager.generate_enemy(enemies)
    # region add levels

    def add_levels(self, *levels: Level):
        for level in levels:
            level.set_levelsystem(self)
        self.levels.extend(levels)

    def add_level(self, level: Level):
        self.levels.append(level)
        level.set_levelsystem(self)

    def insert_level(self, level: Level, level_number: int):
        level.set_levelsystem(self)
        self.levels.insert(level_number-1, level)

    # endregion
