from Scripts.Locals import Face
from Scripts.GameObject.Sprite.Character.Character import Character
from Scripts.CharacterBrain.CharacterBrain import CharacterBrain


class EnemyBrain(CharacterBrain):
    def __init__(self) -> None:
        super().__init__()
        self.target:Character=None

    def set_target(self,target:Character):
        self.target=target
    