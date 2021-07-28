import pygame
from Scripts.Locals import VisualEffectID
from random import randint, random
from time import sleep, time
from pygame.event import peek
import functools

@functools.cache
def add_together(x,y):
    sleep(0.5)
    return x+y
    

import pygame.mixer
pygame.init()
attack= pygame.mixer.Sound("Audios\SoundEffect\Character\Hero\hero_attack.wav")
dead= pygame.mixer.Sound("Audios\SoundEffect\Character\Hero\hero_dead.wav")
underattack= pygame.mixer.Sound("Audios\SoundEffect\Character\Slime\slime_underattack.wav")
for _ in range(10):
    attack.play()
    underattack.play()
    sleep(0.5)
dead.play()
sleep(5)