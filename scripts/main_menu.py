import pygame, os, sys
from scripts.button import *
from scripts.fonts_and_colors import *
from scripts.useful_functions import *

def main_menu(surface, game):
    option = 0
    text1 = 'Super Muki'
    version = '1.5'
    selected = False

    b1_r = pygame.Rect(100, CY, 400, 200)
    b1_s = pygame.Surface((b1_r.width, b1_r.height))

    b2_r = pygame.Rect(W-500, CY, 400, 200)
    b2_s = pygame.Surface((b1_r.width, b1_r.height))

    pygame.mouse.set_visible(True)

    while not selected:
        clock.tick(60)
        pos = pygame.mouse.get_pos()
        surface.fill((0, 0, 80))

        settings_b.draw(surface)

        green_button(b1_s, b1_r, pos)
        green_button(b2_s, b2_r, pos)
        
        surface.blit(b1_s, b1_r)
        surface.blit(b2_s, b2_r)

        mts(surface, True, 60, '1 Player', WHITE, b1_r.centerx, b1_r.centery)
        mts(surface, True, 60, '2 Player', WHITE, b2_r.centerx, b2_r.centery)

        mts(surface, True, 100, text1, WHITE, surface.get_width() // 2, 150)

        mts(surface, False, 30, f'version: {version}', WHITE, 30, H-60)

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT: selected = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: selected = True
                if event.key == pygame.K_1: option = 1; selected = True
                if event.key == pygame.K_2: option = 2; selected = True

            if event.type == pygame.MOUSEBUTTONUP:
                if b1_r.collidepoint(pos): option = 1; selected = True
                if b2_r.collidepoint(pos): option = 2; selected = True
                if settings_b.rect.collidepoint(pos): settings(surface, game)


    game.players = option
    fade(surface)

    pygame.mouse.set_visible(False)

