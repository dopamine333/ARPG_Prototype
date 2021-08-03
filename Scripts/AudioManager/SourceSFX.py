from pygame.mixer import Sound
from Scripts.AudioManager.SFX import SFX


class SourceSFX(SFX):
    def __init__(self,source:Sound,volume:float=0.5) -> None:
        self.source=source
        #TODO 需要控制聲音大小嗎
        self.volume=volume

    def play(self):
        self.source.play()

    def set_volume(self,volume:float):
        self.volume=volume
        if self.source:
            self.source.set_volume(self.volume)

    def set_source(self,source:Sound):
        self.source=source
        self.source.set_volume(self.volume)