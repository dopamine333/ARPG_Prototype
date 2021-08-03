from Scripts.AudioManager.SFX import SFX

from random import choice

class RandomSFX(SFX):
    def __init__(self) -> None:
        self.sfxs:list[SFX]=[]

    def play(self):
        if len(self.sfxs)==0:
            return
        choice(self.sfxs).play()

    def add_SFX(self,sfx:SFX):
        self.sfxs.append(sfx)