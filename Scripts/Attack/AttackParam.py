from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Scripts.GameObject.Sprite.Character.Character import Character
from Scripts.Locals import GameEvent
from Scripts.Managers.EventManager import EventManager
from Scripts.Physics.Collider import Collider
from Scripts.Physics.RigidBody import RigidBody
from Scripts.Graph.Image import Image
from Scripts.GameObject.Sprite.Sprite import Sprite
from pygame import Vector2, Vector3
import pygame.font

class AttackParam:
    def __init__(self,damage: float,force:Vector3) -> None:
        self.damage=damage
        self.force=force
        self.attacker:Character=None
        self.defender:Character=None
    def set_attacker(self,attacker:Character):
        self.attacker=attacker
    def set_defender(self,defender:Character):
        self.defender=defender
    #TODO 也許能做一個Timer，統一管理計時的類   
    #TODO 顯示傷害 
    def show(self):
        pass
        print("attack!",self.damage)
        '''
        font = pygame.font.SysFont("Comic Sans MS", self.damage*5+30, True)
        text= font.render(str(self.damage),True,(220,100,100))
        size=Vector3(text.get_width(),text.get_height(),5)
        damage_text_rigidbody=RigidBody(Collider(size/2,size))
        damage_text_rigidbody.add_force(self.force+Vector3(0,60,0))
        damage_text_rigidbody.set_damp(0.6)
        damage_text_position=(self.attacker.position+self.defender.position)/2
        damage_text_position.y+=20
        damage_text=Sprite(Image(text),damage_text_position,damage_text_rigidbody)
        EventManager.notify(GameEvent.add_gameobject,damage_text)
        '''
