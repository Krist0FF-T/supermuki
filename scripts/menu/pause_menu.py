import pygame as pg
from scripts import button, consts, util
from . import code


def pause_menu(surf) -> int | None:
    resume_r = button.resume_button.rect
    resume_s = pg.Surface((resume_r.width, resume_r.height))

    quit_r = button.quit_button.rect
    quit_s = pg.Surface((quit_r.width, quit_r.height))

    paused = True
    while paused:
        # events
        mpos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                util.close()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    util.close()
                if event.key == pg.K_ESCAPE or event.key == pg.K_c:
                    paused = False

            elif event.type == pg.MOUSEBUTTONUP:
                if resume_r.collidepoint(mpos):
                    paused = False
                if quit_r.collidepoint(mpos):
                    util.close()
                if button.load_lvl_b.rect.collidepoint(mpos):
                    return code.LEVEL_SELECT
                if button.color_s_b.rect.collidepoint(mpos):
                    return code.COLOR_SELECT
                if button.mainm_b.rect.collidepoint(mpos):
                    return code.MAIN_MENU

        consts.clock.tick(consts.FPS)
        surf.fill(consts.GUI_BG_COLOR)

        # draw buttons
        button.load_lvl_b.draw(surf)
        button.color_s_b.draw(surf)

        button.mainm_b.draw(surf)

        button.green_button(resume_s, resume_r, mpos)
        surf.blit(resume_s, resume_r)

        button.green_button(quit_s, quit_r, mpos)
        surf.blit(quit_s, quit_r)

        # draw text
        util.draw_text(surf, True, 100, "Paused!", "white", consts.CX, 150)
        util.draw_text(
            surf,
            True,
            45,
            "Resume (C)",
            "white",
            button.resume_button.rect.centerx,
            button.resume_button.rect.centery,
        )
        util.draw_text(
            surf,
            True,
            45,
            "Quit (Q)",
            "white",
            button.quit_button.rect.centerx,
            button.quit_button.rect.centery,
        )

        pg.display.update()

