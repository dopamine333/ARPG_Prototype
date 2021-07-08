import pygame
import pygame.display
import pygame.time
import pygame.event
import sys
from pygame import Surface,Vector2,Vector3
class GameLoop:
    def __init__(self) -> None:
        self.screen=pygame.display.set_mode((1280,720))
        self.screen_size=Vector2(self.screen.get_size())
        self.clock=pygame.time.Clock()
        
    def run(self):
        running=True
        while running:
            if pygame.QUIT in [event.type for event in pygame.event.get()]:
                running=False
            self.clock.tick(60)

            pygame.display.update()
        pygame.quit()
        sys.exit()
if __name__=="__main__":
    gameLoop=GameLoop()
    gameLoop.run()