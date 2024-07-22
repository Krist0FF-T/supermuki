import pygame as pg
from . import button, consts, util
from .settings import settings


def main_menu(surface, game):
    option = 0
    text1 = 'Super Muki'
    version = '1.5'
    selected = False

    b1_r = pg.Rect(100, consts.CY, 400, 200)
    b1_s = pg.Surface((b1_r.width, b1_r.height))

    b2_r = pg.Rect(consts.W-500, consts.CY, 400, 200)
    b2_s = pg.Surface((b1_r.width, b1_r.height))

    pg.mouse.set_visible(True)

    while not selected:
        consts.clock.tick(60)
        pos = pg.mouse.get_pos()
        surface.fill((0, 0, 80))

        button.settings_b.draw(surface)

        button.green_button(b1_s, b1_r, pos)
        button.green_button(b2_s, b2_r, pos)

        surface.blit(b1_s, b1_r)
        surface.blit(b2_s, b2_r)

        util.draw_text(
            surface, True, 60, '1 Player',
            "white", b1_r.centerx, b1_r.centery
        )

        util.draw_text(
            surface, True, 60, '2 Player',
            "white", b2_r.centerx, b2_r.centery
        )

        util.draw_text(
            surface, True, 100, text1, "white",
            surface.get_width() // 2, 150
        )

        util.draw_text(
            surface, False, 30, f'version: {version}',
            "white", 30, consts.H-60
        )

        pg.display.update()

        for event in pg.event.get():

            if event.type == pg.QUIT:
                selected = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    selected = True
                if event.key == pg.K_1:
                    option = 1
                    selected = True
                if event.key == pg.K_2:
                    option = 2
                    selected = True

            if event.type == pg.MOUSEBUTTONUP:
                if b1_r.collidepoint(pos):
                    option = 1
                    selected = True
                if b2_r.collidepoint(pos):
                    option = 2
                    selected = True
                if button.settings_b.rect.collidepoint(pos):
                    settings(surface, game)

    game.players = option

    pg.mouse.set_visible(False)
