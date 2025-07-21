import pygame as pg
import sys

from . import button, consts, util
from .main_menu import main_menu
from .level_selection import level_selection


def pause(screen, game, players, player1, player2, load_level):
    """
    Handle the pause menu functionality.
    
    Args:
        screen: pygame screen surface
        game: Game instance
        players: list of player objects
        player1: Player 1 object
        player2: Player 2 object  
        load_level: function to load levels
    
    Returns:
        None
    """
    # reset_time_b = Button(0, 100, "simple_b2.png", 12)

    resume_r = button.resume_button.rect
    resume_s = pg.Surface((resume_r.width, resume_r.height))

    quit_r = button.quit_button.rect
    quit_s = pg.Surface((quit_r.width, quit_r.height))
    mm = False  # enter main menu

    paused = True
    while paused:
        pos = pg.mouse.get_pos()
        consts.clock.tick(consts.FPS)
        screen.fill(game.gui_rgb)

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
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    pg.quit()
                if event.key == pg.K_ESCAPE or event.key == pg.K_c:
                    paused = False

            if event.type == pg.MOUSEBUTTONUP:
                if resume_r.collidepoint(pos):
                    paused = False
                if quit_r.collidepoint(pos):
                    pg.quit()
                    sys.exit()
                if button.load_lvl_b.rect.collidepoint(pos):
                    game.load_level_bool = True
                    paused = False
                if button.color_s_b.rect.collidepoint(pos):
                    game.color_selection()
                if button.mainm_b.rect.collidepoint(pos):
                    paused = False
                    mm = True

    if mm:
        main_menu(screen, game)
        if game.players == 2:
            if len(players) < 2:
                players.append(player2)
        else:
            players.clear()
            players.append(player1)

        for p in players:
            p.deaths = 0
        game.color_selection()
        game.level_selected = False
        level_selection(screen, game)

        if game.level_selected:
            load_level(game.level)
        else:
            load_level(1)