import pygame
from Scripts.AudioManager.SourceSFX import SourceSFX
from pygame.mixer import Sound
from Scripts.AudioManager.RandomSFX import RandomSFX
from Scripts.AudioManager.SFX import SFX
from Scripts.Locals import MusicID, SFXID
from Scripts.Tools.Singleton import Singleton
from os.path import join
import pygame.mixer


class AudioManger(Singleton):
    def __init__(self) -> None:
        self.sfxs: dict[SFXID, SFX] = {}
        # self.musics:dict[MusicID,Music]={}
        self.path = ""

        pygame.mixer.init()

        self.set_path("Audios\SoundEffect\Character\Hero")
        self.sfxs[SFXID.hero_attack] = self.load_SFX("hero_attack")
        self.sfxs[SFXID.hero_move] = self.load_SFX("hero_move", 11)
        self.sfxs[SFXID.hero_jump] = self.load_SFX("hero_jump")
        self.sfxs[SFXID.hero_land] = self.load_SFX("hero_land")
        self.sfxs[SFXID.hero_underattack] = self.load_SFX("hero_underattack", 8)
        self.sfxs[SFXID.hero_dead] = self.load_SFX("hero_dead", 5)
        
        self.set_path("Audios\SoundEffect\Character\Slime")
        self.sfxs[SFXID.slime_jump] = self.load_SFX("slime_jump")
        self.sfxs[SFXID.slime_land] = self.load_SFX("slime_land")
        self.sfxs[SFXID.slime_underattack] = self.load_SFX("slime_underattack")
        self.sfxs[SFXID.slime_dead] = self.load_SFX("slime_dead")

    def set_path(self, path: str):
        self.path = path

    def play_SFX(self, sfxID: SFXID):
        self.sfxs[sfxID].play()

    def load_SFX(self, name: str, num: int=1):
        if num==1:
            return SourceSFX(Sound(join(self.path, name)+"-01.wav"))
        randomSFX = RandomSFX()
        for i in range(1, num+1):
            sfx = SourceSFX(Sound(join(self.path, name)+"-"+str(i).zfill(2)+".wav"))
            randomSFX.add_SFX(sfx)
        return randomSFX

        
        
         
    # def play_music(self,music:MusicID):
    #    pass
