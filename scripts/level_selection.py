import sys
import pygame
from json import load
from . import consts, util, button


def level_selection(surface, g):
    button_quit_r = pygame.Rect(50, 50, 160, 90)
    button_quit_s = pygame.Surface((button_quit_r.width, button_quit_r.height))

    lb_width = 120

    cd = 10

    with open("data.json", "r") as f:
        data = load(f)
        completed_levels = data["completed_lvls"]

    b_run_r = pygame.Rect(consts.CX-150, consts.CY-60, 300, 120)
    b_run_s = pygame.Surface((b_run_r.width, b_run_r.height))

    sr_r = pygame.Rect(consts.W-50-250, 50, 250, 90)
    sr_s = pygame.Surface((sr_r.width, sr_r.height))

    b_rows = 2
    b_cols = 5

    selecting_level = True
    while selecting_level:
        consts.clock.tick(60)
        surface.fill(g.gui_rgb)
        pos = pygame.mouse.get_pos()

        if cd >= 1:
            cd -= 1

        if not g.speedrun:
            button.green_button(button_quit_s, button_quit_r, pos)
            surface.blit(button_quit_s, button_quit_r)
            util.draw_text(
                surface, True, 40, "Back", "white",
                button_quit_r.centerx, button_quit_r.centery
            )

        button.green_button(sr_s, sr_r, pos)
        surface.blit(sr_s, sr_r)

        if not g.speedrun:
            for i in range(b_cols):
                for y in range(b_rows):
                    num = i + (y * b_cols) + 1
                    option_r = pygame.Rect(
                        (140 * i) + 300, (140 * y) + 280, lb_width, lb_width)
                    option_s = pygame.Surface(
                        (option_r.width, option_r.height))

                    if completed_levels >= num:
                        option_s.fill((0, 255, 0))
                        if option_r.collidepoint(pos):
                            option_s.fill((120, 255, 120))
                            if cd <= 0 and pygame.mouse.get_pressed()[0]:
                                option_s.fill((50, 50, 50))
                                g.level_to_load = f"{num}"
                                g.level = num
                                g.level_selected = True
                                selecting_level = False
                    else:
                        option_s.fill((120, 120, 120))

                    surface.blit((option_s), option_r)
                    util.draw_text(surface, True, 50, str(num), "white",
                                   option_r.centerx, option_r.centery)

        if g.speedrun and cd <= 0:
            button.colored_b(b_run_s, b_run_r, (0, 255, 0), pos)
            surface.blit(b_run_s, b_run_r)
            util.draw_text(surface, True, 40, "Start",
                           "white", consts.CX, consts.CY)
            if pygame.mouse.get_pressed()[0]:
                if b_run_r.collidepoint(pos):
                    g.reset_deaths()
                    g.reset_timer()

                    g.level_to_load = "1"
                    g.level = 1
                    g.selecting_level = False
                    g.level_selected = True
                    selecting_level = False

        util.draw_text(surface, True, 60, "Level Selection",
                       "white", consts.CX, 90)
        util.draw_text(surface, True, 40, "speedrun",
                       "white", sr_r.centerx, sr_r.centery)
        util.draw_text(surface, True, 40, f"{g.speedrun}",
                       "white", sr_r.centerx, sr_r.centery + 80)

        if g.devmode:
            pygame.draw.line(
                surface,
                "red",
                (consts.CX, 0),
                (consts.CX, consts.H),
                4
            )

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:
                if not g.speedrun:
                    if button_quit_r.collidepoint(pos):
                        g.level_selected = False
                        selecting_level = False
                        g.level_to_load = "1"

                if sr_r.collidepoint(pos):
                    g.speedrun = not g.speedrun
