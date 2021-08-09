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
        self.current_level: Level = None
        self.levels: dict[int, Level] = {}

    def start_game(self):
        self.current_level.start_level()

    def update(self):
        self.current_level.update()

    def get_spawnpoint(self):
        return self.current_level.current_savepoint.spawnpoint

    def generate_enemy(self, enemies: list[tuple[CharacterID, Vector3]]):
        self.gamemanager.generate_enemy(enemies)

    def choice_level(self, level_number: int):
        self.current_level = self.levels[level_number]

    def add_level(self, level: Level, level_number: int):
        self.levels[level_number] = level
        level.set_levelsystem(self)
