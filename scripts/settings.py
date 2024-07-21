import pygame, sys

from scripts.button import *
from scripts.useful_functions import *
from scripts.fonts_and_colors import *

clock = pygame.time.Clock()

def mts(surface, rect, size, smthing, color, x, y):
    text = font(size).render(smthing, 1, color)
    if rect:
        text_rect = text.get_rect(center = (x, y))
        surface.blit((text), text_rect)
    elif not rect:
        surface.blit(text, (x, y))
    return text

def button(surf, boolean, text, y):
    b_r = pygame.Rect(20, y, 30, 30)
    b_s = pygame.Surface((b_r.width, b_r.height))
    if boolean: b_s.fill(GREEN)
    else: b_s.fill((100,100,100))
    surf.blit(b_s, b_r)
    
    mts(surf, False, 30, text, WHITE, 20+40, y)

    return b_r

def settings(surf, g):
    s = g.settings
    settings = True
    while settings:
        pos = pygame.mouse.get_pos()
        clock.tick(60)
        surf.fill(g.gui_rgb)

        
        flip_rect = button(surf, s.flip_when_jump, 'flip', 250)
        deaths_rect = button(surf, s.show_deaths, 'show deaths', 300)
        messages_rect = button(surf, s.screen_messages, 'screen messages', 350)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: settings = False

            if event.type == pygame.MOUSEBUTTONUP:
                if flip_rect.collidepoint(pos): s.flip_when_jump = not s.flip_when_jump
                elif deaths_rect.collidepoint(pos): s.show_deaths = not s.show_deaths
                elif messages_rect.collidepoint(pos): s.screen_messages = not s.screen_messages

        pygame.display.update()
                    
        
