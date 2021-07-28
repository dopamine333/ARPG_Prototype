from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Scripts.GameSystem.GameManager import GameManager

from Scripts.Graphic.RenderManager import RenderManager
from Scripts.Locals import CharacterID, Tag
from Scripts.Factory.FactoryManager import FactoryManager
from Scripts.Character.Character import Character
from Scripts.GameSystem.GameSystem import GameSystem
from Scripts.Camera.CameraController import CameraController


class PlayerSystem(GameSystem):
    def __init__(self, gamemanager: GameManager) -> None:
        super().__init__(gamemanager)

        self.player_characterID = CharacterID.Hero
        self.alive_player: Character = None

    def start(self):
        self.spawn_player()

    def spawn_player(self):
        spawnpoint = self.gamemanager.get_spawnpoint()
        characterfactory = FactoryManager.Instance().get_characterfactory()
        player = characterfactory.create(self.player_characterID)
        player.gameobject.set_position(spawnpoint)
        player.gameobject.set_tag(Tag.player)
        player.gameobject.instantiate()
        self.alive_player = player

        RenderManager.camera.get_component(CameraController).set_target(player)
    def update(self):
        if self.alive_player.is_dead:
            self.spawn_player()
            #FIXME 用觀察者模式讓角色復活時 敵人重新鎖定玩家
            for enemy in self.gamemanager.enemysystem.alive_enemies:
                enemy.brain.set_target(self.alive_player)
    def get_player(self) -> Character:
        return self.alive_player
