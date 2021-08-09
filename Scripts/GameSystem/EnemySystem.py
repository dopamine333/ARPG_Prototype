from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Scripts.GameSystem.GameManager import GameManager
    from Scripts.Character.CharacterBrain.EnemyBrain import EnemyBrain
from Scripts.EventManager.EventManager import EventManager
from Scripts.Character.Character import Character
from Scripts.Factory.FactoryManager import FactoryManager
from pygame import Vector3
from Scripts.Locals import CharacterID, GameEvent, Tag
from Scripts.GameSystem.GameSystem import GameSystem


class EnemySystem(GameSystem):
    def __init__(self, gamemanager: GameManager) -> None:
        super().__init__(gamemanager)
        self.alive_enemies: list[Character] = []
        self.counting_death = False

        EventManager.get(GameEvent.player_dead) + self.clear_enemies

    def generate_enemy(self, enemies: list[tuple[CharacterID, Vector3]]):
        characterfactory = FactoryManager.Instance().get_characterfactory()
        player = self.gamemanager.get_player()
        for enemyID, position in enemies:
            enemy = characterfactory.create(enemyID)
            self.alive_enemies.append(enemy)
            brain: EnemyBrain = enemy.brain
            brain.set_target(player)
            enemy.gameobject.set_tag(Tag.enemy)
            enemy.gameobject.set_position(position)
            enemy.gameobject.instantiate()
        self.counting_death = True

    def update(self):
        if self.counting_death:
            to_del = []
            for enemy in self.alive_enemies:
                if enemy.is_dead:
                    self.enemy_dead(enemy)
                    to_del.append(enemy)
            for del_enemy in to_del:
                self.alive_enemies.remove(del_enemy)
            if len(self.alive_enemies) == 0:
                EventManager.get(GameEvent.enemy_clear).notify()
                self.counting_death = False

    def clear_enemies(self):
        for enemy in self.alive_enemies:
            enemy.destroy()
        self.alive_enemies.clear()
        self.counting_death = False

    def enemy_dead(self, enemy: Character):
        # TODO 敵人死亡特效
        enemy.destroy()
