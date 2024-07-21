import pygame
from scripts.useful_functions import *

def intro(surface):
    intro_img = pygame.image.load('img/intro.png')
    intro_image = pygame.transform.scale(intro_img, (W, H))

    surface.blit(intro_image, (0,0))
    mts(surface, False, 60, 'Loading files...', WHITE, 20, 20)
    pygame.display.update()
    pygame.time.wait(1000)
    long_fade(surface)



