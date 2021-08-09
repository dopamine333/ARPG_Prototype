from Scripts.GameSystem.GameManager import GameManager
from Scripts.GameObject.Component import Component


class GameManagerRunner(Component):
    def __init__(self) -> None:
        super().__init__()
        self.gamemanager = GameManager.Instance()

    def start(self):
        self.gamemanager.start_game()

    def update(self):
        self.gamemanager.update()
