import pygame as pg
from scripts import button, consts, util


def main_menu(surf) -> int:
    text1 = 'Super Muki'
    version = '1.5'
    selected = False

    b1_r = pg.Rect(100, consts.CY, 400, 200)
    b1_s = pg.Surface((b1_r.width, b1_r.height))

    b2_r = pg.Rect(consts.W-500, consts.CY, 400, 200)
    b2_s = pg.Surface((b1_r.width, b1_r.height))

    while not selected:
        consts.clock.tick(60)
        pos = pg.mouse.get_pos()
        surf.fill(consts.GUI_BG_COLOR)

        button.green_button(b1_s, b1_r, pos)
        button.green_button(b2_s, b2_r, pos)

        surf.blit(b1_s, b1_r)
        surf.blit(b2_s, b2_r)

        util.draw_text(
            surf, True, 60, '1 Player',
            "white", b1_r.centerx, b1_r.centery
        )

        util.draw_text(
            surf, True, 60, '2 Player',
            "white", b2_r.centerx, b2_r.centery
        )

        util.draw_text(
            surf, True, 100, text1, "white",
            surf.get_width() // 2, 150
        )

        util.draw_text(
            surf, False, 30, f'version: {version}',
            "white", 30, consts.H-60
        )

        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                util.close()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_1:
                    return 1
                if event.key == pg.K_2:
                    return 2

            if event.type == pg.MOUSEBUTTONDOWN:
                if b1_r.collidepoint(pos):
                    return 1
                if b2_r.collidepoint(pos):
                    return 2

    return 0
