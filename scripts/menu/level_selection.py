import pygame as pg
from scripts import consts, util


def level_selection(surf: pg.Surface) -> int | None:
    lb_width = 120

    b_rows = 2
    b_cols = 5

    selecting_level = True
    while selecting_level:
        consts.clock.tick(60)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                util.close()

        surf.fill(consts.GUI_BG_COLOR)
        mouse_pos = pg.mouse.get_pos()

        for i in range(b_cols):
            for y in range(b_rows):
                num = i + (y * b_cols) + 1
                option_r = pg.Rect(
                    (140 * i) + 300,
                    (140 * y) + 280,
                    lb_width, lb_width
                )
                option_s = pg.Surface((
                    option_r.width, option_r.height
                ))

                option_s.fill("green")
                if option_r.collidepoint(mouse_pos):
                    option_s.fill((120, 255, 120))
                    if pg.mouse.get_just_pressed()[0]:
                        option_s.fill((50, 50, 50))
                        return num

                surf.blit((option_s), option_r)
                util.draw_text(surf, True, 50, str(num), "white",
                               option_r.centerx, option_r.centery)

        util.draw_text(
            surf, True, 60,
            "Level Selection",
            "white", consts.CX, 90
        )

        pg.display.update()

