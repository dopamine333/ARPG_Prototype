from Scripts.Level.GoldSword import GoldSword
from pygame import Vector3


class SavePoint:
    def __init__(self) -> None:
        self.spawnpoint=Vector3()
        self.goldsword: GoldSword=None

        self.next_checkpoint_number=None