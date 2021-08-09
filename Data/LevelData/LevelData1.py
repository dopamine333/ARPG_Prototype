from Scripts.Physics.Box import Box

from Scripts.Level.SavePoint import SavePoint
from Scripts.Level.CheckPoint import Checkpoint
from Scripts.Level.Level import Level

from Scripts.Locals import CharacterID, GameEvent

from pygame import Rect, Surface, Vector3
from random import random

level = Level()
previous_cp: Checkpoint = None
# 檢查點寬度
width = 1500
# 檢查點間隔
space = 1600
# 生成檢查點
for i in range(4):
    x = i*space
    cp = Checkpoint()
    cp.set_trigger_box(Box((10, 10000, 400), (700+x, 5000, 200)))
    cp.set_physics_activity_box(Box((width, 1280, 400), (750+x, 640, 200)))
    cp.set_render_activity_rect(Rect(x, -200, width, 1280))
    trigger_box_sketch = Surface((10, 200))
    trigger_box_sketch.fill((208, 37, 37))
    cp.set_trigger_box_sketch(trigger_box_sketch)
    cp.set_trigger_box_sketch_position(Vector3(695+x, 0, 400))
    cp.set_finish_event(GameEvent.enemy_clear)
    cp.add_enemies(
        *[(CharacterID.slime, (random()*width+x, 0, random()*400)) for _ in range(3, 8)])
    level.add_checkpoint(cp)
# 生成存檔點
for i in range(4):
    if i % 2 == 1:
        continue
    x = i*space
    sp = SavePoint()
    sp.set_spawnpoint(Vector3(420+x, 0, 200))
    sp.set_goldsword_position(Vector3(400+x, 0, 300))
    level.add_savepoint(sp)
    if i == 0:
        level.set_default_savepoint(sp)


def read():
    '''回傳關卡資料'''
    return level
