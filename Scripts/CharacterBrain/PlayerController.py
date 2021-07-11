
import pygame
from Scripts.Managers.EventManager import EventManager
from pygame import Vector2, encode_file_path
from Scripts.Locals import InputEvent
from Scripts.CharacterBrain.CharacterBrain import CharacterBrain
import pygame.key

class PlayerController(CharacterBrain):
    def start(self):
        EventManager.attach(InputEvent.key_down,self.handle)

    def update(self):
        movement=Vector2()
        key_input = pygame.key.get_pressed()
        if key_input[pygame.K_w]:
            movement.y+=1
        if key_input[pygame.K_s]:
            movement.y+=-1
        if key_input[pygame.K_a]:
            movement.x+=-1
        if key_input[pygame.K_d]:
            movement.x+=1
        if movement.xy!=(0,0):
            self.character.move(movement)

    def handle(self,key:InputEvent):
        if key==InputEvent.j:
            self.character.jump()
        if key==InputEvent.k:
            self.character.attack()
        '''#region handle move
        if key == InputEvent.w:
            self.character.move(Vector2(0,1))
            return
        if key == InputEvent.s:
            self.character.move(Vector2(0,-1))
            return
        if key == InputEvent.a:
            self.character.move(Vector2(-1,0))
            return
        if key == InputEvent.d:
            self.character.move(Vector2(1,0))
            return
        #endregion
        '''

