from time import time
from typing import AsyncGenerator

from pygame.time import Clock, wait


#target_fps=60
a,v,x=0,0,0
start=time()
last=time()
clock=Clock()
class Ball:
    def __init__(self) -> None:
        self.ia=0
        self.fa=0
        self.v=0
        self.x=0
    def addforce(self,force,mode):
        if mode == "i":
            self.ia+=force
        if mode == "f":
            self.fa+=force
    def update(self,dt):
        self.v+=self.ia+self.fa*dt
        self.x+=self.v*dt
        self.ia=0
        self.fa=0
    def __repr__(self) -> str:
        return f"a = {round( self.fa+self.ia,4)} v = {round( self.v,4)} a = {round( self.x,4)}"
fps=60
dt=1/fps
b=Ball()
for i in range(fps):
    if i==5:
        b.addforce(10,"i")
    b.addforce(50,"f")
    print(b)
    b.update(dt)