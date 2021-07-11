from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Scripts.GameObject.Sprite.Character.Character import Character

#TODO 完成CharacterBrain的類別圖
class CharacterBrain:  
    def __init__(self) -> None:
        self.character: Character = None

    def set_character(self, character: Character):
        self.character = character

    def start(self):
        pass
    def update(self):
        pass

    def end(self):
        pass
