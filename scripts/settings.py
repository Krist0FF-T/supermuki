import pygame as pg
import sys

from scripts import util, consts


def button(surf, boolean, text, y):
    b_r = pg.Rect(20, y, 30, 30)
    b_s = pg.Surface((b_r.width, b_r.height))
    if boolean:
        b_s.fill(consts.GREEN)
    else:
        b_s.fill((100, 100, 100))
    surf.blit(b_s, b_r)

    util.draw_text(surf, False, 30, text, consts.WHITE, 20+40, y)

    return b_r


def settings(surf, g):
    settings = True
    while settings:
        pos = pg.mouse.get_pos()
        consts.clock.tick(60)
        surf.fill(g.gui_rgb)

        flip_rect = button(surf, g.flip_when_jump, 'flip', 250)
        deaths_rect = button(surf, g.show_deaths, 'show deaths', 300)
        messages_rect = button(surf, g.screen_messages, 'screen messages', 350)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    settings = False

            if event.type == pg.MOUSEBUTTONUP:
                if flip_rect.collidepoint(pos):
                    g.flip_when_jump = not g.flip_when_jump
                elif deaths_rect.collidepoint(pos):
                    g.show_deaths = not g.show_deaths
                elif messages_rect.collidepoint(pos):
                    g.screen_messages = not g.screen_messages

        pg.display.update()
