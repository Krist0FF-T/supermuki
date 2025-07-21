import pygame as pg
import sys

from . import button, consts, util


def pause(screen):
    """
    Handle the pause menu functionality.
    
    Args:
        screen: pygame screen surface
    
    Returns:
        str: Action taken by user - 'resume', 'main_menu', 'load_level', 'color_selection', or 'quit'
    """
    # reset_time_b = Button(0, 100, "simple_b2.png", 12)

    resume_r = button.resume_button.rect
    resume_s = pg.Surface((resume_r.width, resume_r.height))

    quit_r = button.quit_button.rect
    quit_s = pg.Surface((quit_r.width, quit_r.height))

    paused = True
    while paused:
        pos = pg.mouse.get_pos()
        consts.clock.tick(consts.FPS)
        screen.fill((0, 0, 80))  # Standard GUI background color

        # draw buttons
        button.load_lvl_b.draw(screen)
        button.color_s_b.draw(screen)

        button.mainm_b.draw(screen)

        button.green_button(resume_s, resume_r, pos)
        screen.blit(resume_s, resume_r)

        button.green_button(quit_s, quit_r, pos)
        screen.blit(quit_s, quit_r)

        # draw text
        util.draw_text(screen, True, 100, "Paused!",
                       "white", consts.CX, 150)
        util.draw_text(
            screen, True, 45, "Resume (C)", "white",
            button.resume_button.rect.centerx,
            button.resume_button.rect.centery
        )
        util.draw_text(
            screen, True, 45, "Quit (Q)", "white",
            button.quit_button.rect.centerx, button.quit_button.rect.centery
        )

        pg.display.update()

        # events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 'quit'
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    return 'quit'
                if event.key == pg.K_ESCAPE or event.key == pg.K_c:
                    return 'resume'

            if event.type == pg.MOUSEBUTTONUP:
                if resume_r.collidepoint(pos):
                    return 'resume'
                if quit_r.collidepoint(pos):
                    return 'quit'
                if button.load_lvl_b.rect.collidepoint(pos):
                    return 'load_level'
                if button.color_s_b.rect.collidepoint(pos):
                    return 'color_selection'
                if button.mainm_b.rect.collidepoint(pos):
                    return 'main_menu'