import pygame
import pygame.image
import pygame.display
import pygame.event
import pygame.mouse
path=r"D:\code_lab\pygame_lab\ARPG_Prototype\Arts\Character\slime\Slime_Sprite_Sheet.png"
pygame.init()
suf=pygame.image.load(path)
screen=pygame.display.set_mode(suf.get_size())
while True:
    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            pygame.quit()
        if e.type==pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())

    screen.blit(suf,(0,0))
    pygame.display.update()

(222-38, 499-125)