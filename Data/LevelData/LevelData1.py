from Scripts.Level.SavePoint import SavePoint
from Scripts.Locals import CharacterID, GameEvent
from pygame import Rect, Surface, Vector3
from Scripts.Physics.Box import Box
from Scripts.Level.CheckPoint import Checkpoint
from Scripts.Level.Level import Level
from random import random,randint

level=Level()
previous_cp:Checkpoint=None
for i in range(7):
    x=i*1500
    cp=Checkpoint()
    cp.set_trigger_box(Box((10,10000,400),(700+x,5000,200)))
    cp.set_physics_activity_box(Box((2000,1280,400),(1000+x,640,200)))
    cp.set_render_activity_rect(Rect(x,-200,2000,1280))
    trigger_box_sketch=Surface((10,200))
    trigger_box_sketch.fill((208,37,37))
    cp.set_trigger_box_sketch(trigger_box_sketch)
    cp.set_trigger_box_sketch_position(Vector3(695+x,0,400))
    cp.set_finish_event(GameEvent.enemy_clear)
    cp.add_enemies(*[(CharacterID.Slime,(random()*2000+x,0,random()*400)) for _ in range(3,8)])
    level.add_checkpoint(cp)
    
sp=SavePoint()
sp.next_checkpoint_number=1
sp.spawnpoint=Vector3(400,0,300)
level.add_savepoint(sp)
level.set_default_savepoint(sp)
def read():
    return level