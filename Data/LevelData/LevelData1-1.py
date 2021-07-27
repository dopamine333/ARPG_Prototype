from Scripts.Locals import CharacterID
from pygame import Rect
from Scripts.Physics.Box import Box
from Scripts.Level.CheckPoint import Checkpoint
from Scripts.Level.Level import Level
from random import random,randint

level=Level()
for i in range(7):
    x=i*1500
    cp=Checkpoint()
    cp.trigger_box=Box((10,10000,400),(700+x,5000,200))
    cp.physics_activity_box=Box((2000,1280,400),(1000+x,640,200))
    cp.render_activity_rect=Rect(x,1280,2000,1280)
    for _ in range(randint(3,8)):
        cp.enemies.append((CharacterID.Slime,(random()*2000+x,0,random()*400)))
    level.add_checkpoint()

def read():
    return level