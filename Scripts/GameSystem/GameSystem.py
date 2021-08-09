from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Scripts.GameSystem.GameManager import GameManager


class GameSystem:
    def __init__(self, gamemanager: GameManager) -> None:
        self.gamemanager = gamemanager

    '''def start(self):
        pass'''

    def start_game(self):
        pass

    def update(self):
        pass

    '''def end(self):
        pass'''
