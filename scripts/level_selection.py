import sys
import pygame as pg
from . import consts, util, button


def level_selection(surface, g):
    button_quit_r = pg.Rect(50, 50, 160, 90)
    button_quit_s = pg.Surface((button_quit_r.width, button_quit_r.height))

    lb_width = 120

    # 10 frame countdown after mouse key press
    cd = 10

    sr_r = pg.Rect(consts.W-50-250, 50, 250, 90)
    sr_s = pg.Surface((sr_r.width, sr_r.height))

    b_rows = 2
    b_cols = 5

    selecting_level = True
    while selecting_level:
        consts.clock.tick(60)
        surface.fill(g.gui_rgb)
        pos = pg.mouse.get_pos()

        if cd > 0:
            cd -= 1

        button.green_button(button_quit_s, button_quit_r, pos)
        surface.blit(button_quit_s, button_quit_r)
        util.draw_text(
            surface, True, 40, "Back", "white",
            button_quit_r.centerx, button_quit_r.centery
        )

        button.green_button(sr_s, sr_r, pos)
        surface.blit(sr_s, sr_r)

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

                option_s.fill(consts.GREEN)
                if option_r.collidepoint(pos):
                    option_s.fill((120, 255, 120))
                    if cd <= 0 and pg.mouse.get_pressed()[0]:
                        option_s.fill((50, 50, 50))
                        g.level_to_load = f"{num}"
                        g.level = num
                        g.level_selected = True
                        selecting_level = False

                surface.blit((option_s), option_r)
                util.draw_text(surface, True, 50, str(num), "white",
                               option_r.centerx, option_r.centery)

        util.draw_text(
            surface, True, 60,
            "Level Selection",
            consts.WHITE, consts.CX, 90
        )

        if g.devmode:
            pg.draw.line(
                surface,
                "red",
                (consts.CX, 0),
                (consts.CX, consts.H),
                4
            )

        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.MOUSEBUTTONUP:
                if button_quit_r.collidepoint(pos):
                    g.level_selected = False
                    selecting_level = False
                    g.level_to_load = "1"
