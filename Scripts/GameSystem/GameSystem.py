from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Scripts.GameSystem.GameManager import GameManager


class GameSystem:
    def __init__(self, gamemanager: GameManager) -> None:
        self.gamemanager = gamemanager

    def init(self):
        pass

    def start(self):
        pass

    def update(self):
        pass

    def release(self):
        pass
