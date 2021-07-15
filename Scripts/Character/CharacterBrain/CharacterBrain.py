from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Scripts.Character.Character import Character


class CharacterBrain:
    '''
    控制角色(Character)

    根據不同狀態控制角色的行為
    '''

    def __init__(self) -> None:
        self.character: Character = None

    def start(self):
        pass

    def update(self):
        pass

    def end(self):
        pass
