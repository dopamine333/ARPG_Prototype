from Scripts.Level.GoldSword import GoldSword
from pygame import Vector3


class SavePoint:
    def __init__(self) -> None:
        self.rebirthpoint=Vector3()
        self.goldsword: GoldSword=None