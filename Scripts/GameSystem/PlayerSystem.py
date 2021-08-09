from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Scripts.GameSystem.GameManager import GameManager

from Scripts.EventManager.EventManager import EventManager
from Scripts.Graphic.RenderManager import RenderManager
from Scripts.Locals import CharacterID, GameEvent, Tag
from Scripts.Factory.FactoryManager import FactoryManager
from Scripts.Character.Character import Character
from Scripts.GameSystem.GameSystem import GameSystem
from Scripts.Camera.CameraController import CameraController


class PlayerSystem(GameSystem):
    def __init__(self, gamemanager: GameManager) -> None:
        super().__init__(gamemanager)

        self.player_characterID = CharacterID.hero
        self.alive_player: Character = None

    def start_game(self):
        self.spawn_player()

    def spawn_player(self):
        spawnpoint = self.gamemanager.get_spawnpoint()
        characterfactory = FactoryManager.Instance().get_characterfactory()
        player = characterfactory.create(self.player_characterID)
        player.gameobject.set_position(spawnpoint)
        player.gameobject.set_tag(Tag.player)
        player.gameobject.instantiate()
        self.alive_player = player

        RenderManager.camera.get_component(
            CameraController).set_target(player.position)

    def update(self):
        if self.alive_player.is_dead:
            EventManager.notify(GameEvent.player_dead)
            self.spawn_player()

    def get_player(self) -> Character:
        return self.alive_player
