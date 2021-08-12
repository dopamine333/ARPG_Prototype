from Scripts.GameSystem.GameManager import GameManager
from Scripts.GameObject.Component import Component


class GameManagerRunner(Component):
    def __init__(self) -> None:
        super().__init__()
        self.gamemanager = GameManager.Instance()

    def start(self):
        self.gamemanager.init()
        self.gamemanager.start()

    def update(self):
        self.gamemanager.update()

    def on_destroy(self):
        self.gamemanager.release()