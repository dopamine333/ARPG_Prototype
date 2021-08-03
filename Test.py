import pygame
from Scripts.Locals import VFXID
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
attack= pygame.mixer.Sound("Audios\SoundEffect\Character\Hero\hero_attack-01.wav")
dead= pygame.mixer.Sound("Audios\SoundEffect\Character\Hero\hero_dead-01.wav")
underattack= pygame.mixer.Sound("Audios\SoundEffect\Character\Slime\slime_jump-01.wav")
for _ in range(10):
    dead.set_volume(0.5)
    dead.play()
    sleep(0.5)
    dead.play()
    print("play")
    sleep(2)
    dead.stop()
    #underattack.play()
    sleep(3)
dead.play()
sleep(5)