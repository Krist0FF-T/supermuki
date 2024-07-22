from random import randint, choice
import random
import pygame as pg
import json
import sys
from math import sin, cos, atan2, hypot

from scripts.button import *
from scripts.settings import settings
from scripts.level_selection import *
from scripts.main_menu import main_menu
from scripts.util import *
from scripts.consts import *
from scripts.assets import asset_manager

with open("data.json", "r") as f:
    data = json.load(f)

fullscreen = data["auto_fullscreen"]
vsync = data["vsync"]

screen = pg.display.set_mode((W, H), vsync=vsync)
pg.display.set_caption("SuperMuki")

asset_manager.load_player_imgs("player")

fly = False


class Settings:
    def __init__(self):
        self.flip_when_jump = True
        self.show_deaths = True
        self.screen_messages = False


settings_obj = Settings()


class Game:
    def __init__(self):

        self.devmode = False
        self.leveltest = True

        self.settings = settings_obj
        self.gui_rgb = (0, 0, 80)
        self.num_of_levels = 15
        self.level = 1
        self.loadlevel_bool = False
        self.level_selected = False

        self.players = 1
        self.stop_player_move = False
        self.speedrun = False
        self.t_mval, self.t_sec, self.t_min = 0, 0, 0

    def reset_timer(self):
        self.t_mval, self.t_sec, self.t_min = 0, 0, 0

    def reset_deaths(self):
        for player in players:
            player.alive = True
            player.deaths = 0

    def color_selection(self):
        c_s = True
        lines = [[RED, 200, 300, 450],
                 [GREEN, 200, 410, 450],
                 [BLUE, 200, 520, 450]]

        if game.players == 2:
            lines.append([RED,   W-450, 300, W-200])
            lines.append([GREEN, W-450, 410, W-200])
            lines.append([BLUE,  W-450, 520, W-200])

        c_b1 = [p1_red, p1_green, p1_blue]
        c_b2 = [p2_red, p2_green, p2_blue]

        confirm_r = confirm_c.rect
        confirm_s = pg.Surface((confirm_r.width, confirm_r.height))

        pg.mouse.set_visible(True)
        while c_s:
            clock.tick(120)
            screen.fill((50, 50, 50))
            pos = pg.mouse.get_pos()
            colored_b(confirm_s, confirm_r, [80, 80, 80], pos)
            screen.blit(confirm_s, confirm_r)
            draw_text(screen, True, 30, "Done", WHITE,
                confirm_r.centerx, confirm_r.centery)

            for li in lines:
                pg.draw.line(screen, li[0], [li[1], li[2]], [
                                 li[3], li[2]], 7)

            for bu1 in c_b1:
                bu1.draw(screen)
            if game.players == 2:
                for bu2 in c_b2:
                    bu2.draw(screen)

            for i in range(3):
                if c_b1[i].rect.left < 200:
                    c_b1[i].rect.left = 200
                if c_b1[i].rect.right > 450:
                    c_b1[i].rect.right = 450

                if game.players == 2:
                    if c_b2[i].rect.left < W-450:
                        c_b2[i].rect.left = W-450
                    if c_b2[i].rect.right > W-200:
                        c_b2[i].rect.right = W-200

                player1.color[i] = c_b1[i].rect.centerx - 200
                if game.players == 2:
                    player2.color[i] = c_b2[i].rect.centerx - (W-450)

            settings_b.draw(screen)

            player1.images = []
            for c_img in asset_manager.player_images:
                p_img = palette_swap(c_img, c_img.get_at(
                    (0, 0)), player1.color).convert()
                p_img.set_colorkey((0, 0, 0))
                player1.images.append(p_img)

            if game.players == 2:
                player2.images = []
                for c_img in asset_manager.player_images:
                    p_img = palette_swap(c_img, c_img.get_at(
                        (0, 0)), player2.color).convert()
                    p_img.set_colorkey((0, 0, 0))
                    player2.images.append(p_img)

            p1_pv_image = pg.transform.scale(player1.images[2], (80, 80))
            p1_pv_rect = p1_pv_image.get_rect()
            p1_pv_rect.center = 350, 120

            p2_pv_image = pg.transform.scale(player2.images[2], (80, 80))
            p2_pv_rect = p2_pv_image.get_rect()
            p2_pv_rect.center = W - 350, 120

            screen.blit((p1_pv_image), p1_pv_rect)
            if game.players == 2:
                screen.blit((p2_pv_image), p2_pv_rect)

            draw_text(screen, True, 30, str(player1.color),
                WHITE, p1_pv_rect.centerx, H-100)
            if game.players == 2:
                draw_text(screen, True, 30, str(player2.color),
                    WHITE, p2_pv_rect.centerx, H-100)

            pg.display.update()

            if pg.mouse.get_pressed()[0]:
                for bu in c_b1:
                    if pg.Rect(bu.rect.x-25, bu.rect.y-25, bu.rect.width+50, bu.rect.height+50).collidepoint(pos):
                        bu.rect.centerx = pos[0]
                    if bu.rect.left < 200:
                        bu.rect.left = 200
                    if bu.rect.right > 450:
                        bu.rect.right = 450

                if game.players == 2:
                    for bu in c_b2:
                        if pg.Rect(bu.rect.x-20, bu.rect.y-20, bu.rect.width+40, bu.rect.height+40).collidepoint(pos):
                            bu.rect.centerx = pos[0]
                        if bu.rect.left < W-450:
                            bu.rect.left = W-450
                        if bu.rect.right > W-200:
                            bu.rect.right = W-200

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key in [pg.K_SPACE, pg.K_ESCAPE]:
                        fade(screen)
                        c_s = False

                if event.type == pg.MOUSEBUTTONDOWN:
                    if confirm_c.rect.collidepoint(pos):
                        fade(screen)
                        c_s = False
                    if settings_b.rect.collidepoint(pos):
                        settings(screen, game)


game = Game()
g = game


def pause(surface=screen, g=game):
    # reset_time_b = Button(0, 100, "simple_b2.png", 12)

    resume_r = resume_button.rect
    resume_s = pg.Surface((resume_r.width, resume_r.height))

    quit_r = quit_button.rect
    quit_s = pg.Surface((quit_r.width, quit_r.height))
    mm = False  # enter main menu

    pg.mouse.set_visible(True)
    paused = True
    while paused:
        pos = pg.mouse.get_pos()
        clock.tick(FPS)
        surface.fill(g.gui_rgb)

        # draw buttons
        settings_b.draw(surface)
        load_lvl_b.draw(surface)
        color_s_b.draw(surface)

        mainm_b.draw(surface)

        green_button(resume_s, resume_r, pos)
        surface.blit(resume_s, resume_r)

        green_button(quit_s, quit_r, pos)
        surface.blit(quit_s, quit_r)

        # draw text
        draw_text(surface, True, 100, "Paused!", WHITE, CX, 150)
        draw_text(surface, True, 45, "Resume (C)", WHITE,
            resume_button.rect.centerx, resume_button.rect.centery)
        draw_text(surface, True, 45, "Quit (Q)", WHITE,
            quit_button.rect.centerx, quit_button.rect.centery)

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
                if settings_b.rect.collidepoint(pos):
                    settings(surface, game)
                if load_lvl_b.rect.collidepoint(pos):
                    g.loadlevel_bool = True
                    paused = False
                if color_s_b.rect.collidepoint(pos):
                    g.color_selection()
                if mainm_b.rect.collidepoint(pos):
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
            loadlevel(game.level)
        else:
            loadlevel(1)
    else:
        pg.mouse.set_visible(False)


def game_over(cause):
    game_over = True
    fade(screen)
    restart = Button(CX, CY + 30, "simple_b2.png", 24)
    restart_game = False
    pg.mouse.set_visible(True)
    g.stop_player_move = True

    while game_over:
        pos = pg.mouse.get_pos()
        clock.tick(FPS)
        screen.fill((50, 50, 50))

        settings_b.draw(screen)
        restart.draw(screen)

        draw_text(screen, True, 60, f"level failed", RED, CX, 80)
        draw_text(screen, True, 40, f"({cause})", WHITE, CX, 180)
        draw_text(screen, True, 60, f"retry", WHITE,
            restart.rect.centerx, restart.rect.centery)

        pg.display.update()

        if restart_game:
            loadlevel(game.level, True)
            game.stop_player_move = True
            for p in players:
                p.alive = True
                p.rect.topleft = p.rpp
            game_over = False

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    restart_game = True
                if event.key == pg.K_ESCAPE:
                    pause(screen, game)
            if event.type == pg.MOUSEBUTTONDOWN:
                if restart.rect.collidepoint(pos):
                    restart_game = True
                if settings_b.rect.collidepoint(pos):
                    settings(screen, game)
    pg.mouse.set_visible(False)


def victory():
    victory = True
    restart_r = pg.Rect(CX-160, CY-100, 320, 120)
    restart_s = pg.Surface((restart_r.width, restart_r.height))
    restart_game = False
    pg.mouse.set_visible(True)

    rcl_r = pg.Rect(CX-160, restart_r.bottom+20, 320, 120)
    rcl_s = pg.Surface((rcl_r.width, rcl_r.height))
    confirm_reset = False

    while victory:
        pos = pg.mouse.get_pos()
        clock.tick(FPS)
        screen.fill(game.gui_rgb)

        settings_b.draw(screen)

        green_button(restart_s, restart_r, pos)
        screen.blit(restart_s, restart_r)

        green_button(rcl_s, rcl_r, pos)
        screen.blit(rcl_s, rcl_r)

        draw_text(screen, True, 30, "deaths", WHITE, W - 80, 30)
        if game.players == 1:
            draw_text(screen, True, 30, f"{player1.deaths}",
                player1.color, W - 80, 90)

        elif game.players == 2:
            for player in players:
                draw_text(screen, True, 30, f"{player.deaths}",
                    player.color, W-200+(80*player.num), 90)

        draw_text(screen, True, 60, f"Thx for playing!", WHITE, CX, 100)
        draw_text(screen, True, 40, "play again", WHITE,
            restart_r.centerx, restart_r.centery)
        draw_text(screen, True, 40, "reset lvls", WHITE, rcl_r.centerx, rcl_r.centery)

        if game.speedrun:
            draw_text(screen, True, 40, f"time {g.t_min}:{g.t_sec}.{
                int(g.t_mval/6.5)}", WHITE, CX, H-70)

        if confirm_reset:
            screen.fill(game.gui_rgb)
            draw_text(screen, True, 80, "confirm reset?", WHITE, CX, CY - 100)
            draw_text(screen, True, 60, "[y] yes, [n] no", WHITE, CX, CY + 100)
            keys = pg.key.get_pressed()
            if keys[pg.K_n]:
                confirm_reset = False
            elif keys[pg.K_y]:
                game.reset_timer()
                game.reset_deaths()
                with open("data.json", "r+") as f:
                    data["completed_lvls"] = 1
                    json.dump(data, f)
                game.level_selected = False
                level_selection(screen, game)

                if game.level_selected:
                    loadlevel(game.level)
                else:
                    loadlevel(1)
                for p in players:
                    p.jump = False
                    p.vel_y = 0
                    p.rect.topleft = p.rpp
                victory = False

        pg.display.update()

        if restart_game:
            game.reset_deaths()
            game.stop_player_move = True
            game.level = 1
            victory = False
            loadlevel(game.level)
            for p in players:
                p.alive = True
                p.jump = False
                p.vel_y = 0
                p.rect.topleft = p.rpp
            game.reset_timer()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    restart_game = True
                if event.key == pg.K_ESCAPE:
                    pause(screen, game)
            if event.type == pg.MOUSEBUTTONUP:
                if restart_r.collidepoint(pos):
                    restart_game = True
                if settings_b.rect.collidepoint(pos):
                    settings(screen, game)
                if rcl_r.collidepoint(pos):
                    confirm_reset = True
    pg.mouse.set_visible(False)


def stats_display():
    draw_text(screen, False, 30, f"level {g.level}", WHITE, 15, 15)

    if fly:
        draw_text(screen, True, 20, "fly", WHITE, CX, 30)

    if game.speedrun:
        game.t_mval += 1
        if game.t_mval >= FPS:
            game.t_sec += 1
            game.t_mval = 0
        if game.t_sec >= 60:
            game.t_min += 1
            game.t_sec = 0
        draw_text(screen, False, 30, f"time {g.t_min}:{g.t_sec}", WHITE, 15, 70)

    if game.settings.show_deaths:
        draw_text(screen, True, 30, "deaths", WHITE, W - 80, 30)
        if game.players == 1:
            draw_text(screen, True, 30, f"{player1.deaths}",
                player1.color, W - 80, 90)

        elif game.players == 2:
            for player in players:
                draw_text(screen, True, 30, f"{player.deaths}",
                    player.color, W-200+(80*player.num), 90)


class Camera:
    def __init__(self):
        self.x = 0
        self.target_x = 0
        self.float_x = 0

        self.y = 0
        self.target_y = 0
        self.float_y = 0

    def update(self):
        if game.players == 2:
            self.target_x = - \
                ((player1.rect.centerx + player2.rect.centerx) / 2) + CX
            # self.target_y = -((player1.rect.centery + player2.rect.centery) /2) + CY

        elif game.players == 1:
            self.target_x = -player1.rect.centerx + CX
            # self.target_y = -player1.rect.centery + CY

        self.float_x += (self.target_x - self.float_x)*0.05
        self.x = int(self.float_x)

        self.float_y += (self.target_y - self.float_y)*0.05
        self.y = int(self.float_y)

        if self.x > 0:
            self.x = 0
        if self.x < -4720:
            self.x = -4720


cam = Camera()

left,  right = False, False
left2, right2 = False, False


class Player:
    def __init__(self, num):

        # graphical -----
        self.images = []
        for img in asset_manager.player_images:
            self.images.append(img)

        self.frame_index = 1
        self.animation_cd = 0

        self.color = [255, 0, 0]
        self.flip = False
        self.rotation = 0
        self.rotating = False

        # logical -------
        self.num = num
        self.atj = False
        self.rect = self.images[0].get_rect()
        self.direction = 1

        # - movement
        self.speed = player_speed
        self.knockback = 0
        self.jump = False
        self.vel_y = 0

        # - alive
        self.alive = True
        self.deaths = 0
        self.rpp = (0.0, 0.0)

    def update(self):
        self.flip = (self.direction == -1)

        if self.rect.bottom > ROW*TS:
            self.deaths += 1
            cause = choice(["died", "deaths++", "dropped out of the world"])
            game_over(f"P{self.num} {cause}")

        if self.alive == False:
            self.deaths += 1
            cause = choice(
                ["wanted go back to the respawn point", "died", "didn\"t like life"])

            game_over(f"P{self.num} {cause}")

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > 6000:
            self.rect.right = 6000

    def move(self, left, right):
        dx = 0
        dy = 0

        if left and not right:
            dx = -self.speed
            self.direction = -1

        if right and not left:
            dx = self.speed
            self.direction = 1

        if self.jump and (fly or self.atj):
            self.vel_y = -10
            self.rotating = True
            self.jump = False

        if left or right and self.atj:
            self.animation_cd += 1
            if self.animation_cd >= 7:
                e = {1: 2, 2: 1, 3: 1}
                self.frame_index = e[self.frame_index]
                self.animation_cd = 0
        else:
            self.frame_index = 3

        if self.rotating:
            if settings_obj.flip_when_jump:
                self.rotation -= 15
                if abs(self.rotation) > 355:
                    self.rotation = 0
                    self.rotating = False
            else:
                self.rotating = False

        self.vel_y += GRAVITY
        dy += self.vel_y
        dx += self.knockback

        for block in collideblocks:
            if block[2] == "moving":
                if block[0].colliderect(self.rect.x + dx, self.rect.y + dy + 10, self.rect.width, self.rect.height) and self.vel_y > -1:
                    if self.vel_y > 0:
                        self.vel_y = 0
                        self.atj = True
                        dy = block[0].top - self.rect.bottom

                    dx = block[3]["speed"] * block[3]["direction"]
            if block[2] in solid_blocks:
                if block[0].colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                    if block[2] == "box": # and self.atj:
                        dx = int(dx*0.3)
                        x_collide = False
                        for col_block in blocks:
                            if col_block != block:
                                if col_block[0].colliderect(block[0][0] + dx, block[0][1], TS, TS) or block[0].x < 0:
                                    x_collide = True

                        if x_collide:
                            dx = 0
                        # block[0].x += dx
                        block[3]["dx"] += dx

                    else:
                        dx = 0
                    self.knockback = 0
                if block[0].colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                    if self.vel_y <= 0:
                        self.vel_y = 0
                        dy = block[0].bottom - self.rect.top

                    else:
                        if block[2] == "falling":
                            block[3]["state"] = "fall"

                        self.vel_y = 0
                        self.atj = True
                        dy = block[0].top - self.rect.bottom
                        self.rotating = False
                        self.rotation = 0

                    cam.x += 300

        if abs(self.vel_y) >= 5:
            self.atj = False

        self.rect.x += dx
        self.rect.y += dy

    def velrect(self): return pg.Rect(
        self.rect.x, self.rect.y + self.vel_y, self.rect.width, self.rect.height)

    def explode(self):
        cam.x = cam.target_x
        cam.update()
        di = 10000
        self.rect.centerx -= di
        reDraw()
        sc = screen.copy()
        surfaces = []

        posses = []
        # 3 + 1
        for i in range(1, 4):
            for j in range(1, 4):
                posses.append([-(i*9), -(j*9)])

        # posses = [[0, 0], [-9, 0], [-18, 0],
        #           [0, -9], [-9, -9], [-18, -9],
        #           [0, -18], [-9, -18], [-18, -18]]

        # posses = #[[0, 0], [-13, 0], [0, -13], [-13, -13]]
        img = self.images[0]  # .convert_alpha()

        for i in range(len(posses)*10):
            i %= len(posses)
            # e = pg.Surface((9, 9))
            # e.blit(img, posses[i])
            e = img
            e.set_colorkey(BLACK)
            # -120 = -20
            p = [self.rect.centerx +
                 randint(-15, 15), self.rect.centery+randint(-15, 15)]
            # ra = atan2(self.rect.centery-p[1], self.rect.centerx-p[0])
            ra = random.random() * 2 * 3.1416
            d = [cos(ra)*2, sin(ra)-randint(5, 10)]
            d = [d[0]*5, d[1]*2]
            surfaces.append(
                [e, [self.rect.centerx+di, self.rect.centery], d, 0, -d[0]*2])

        for i in range(120):
            clock.tick(FPS)
            screen.blit(sc, (0, 0))

            for s in surfaces:
                s[3] += s[4]
                d_surf = s[0].copy()
                c_surf = pg.transform.rotate(d_surf, s[3])
                c_surf.set_colorkey((0, 0, 0))
                s[2][1] += GRAVITY
                s[1][0] += s[2][0]
                s[1][1] += s[2][1]
                screen.blit(c_surf, (s[1][0]+cam.x, s[1][1]))

            pg.display.update()
        g.stop_player_move = True

    def draw(self):
        c_img = self.images[self.frame_index-1]
        if self.rect.top < 0:
            fallpos_image = c_img.copy()
            fallpos_image.set_alpha(80)
            screen.blit(flip(fallpos_image, self.flip),
                        (self.rect.x + cam.x, 30))

        if settings_obj.flip_when_jump:
            img_to_blit = pg.transform.rotate(c_img, self.rotation)

        else:
            img_to_blit = c_img

        # screen.blit(flip(img_to_blit, self.flip),
        #             (self.rect.x+cam.x, self.rect.y+cam.y))

        flipped = flip(img_to_blit, self.flip)
        rect = flipped.get_rect()
        rect.centerx = self.rect.centerx + cam.x
        rect.centery = self.rect.centery + cam.y
        screen.blit(flipped, rect)


solid_blocks = ["grass", "dirt", "shooter", "box", "falling", "sticky"]
moving_blocks = ["moving", "enemy"]

collideblocks = []
reset_blocks = []

blocks = []
bg_blocks = []
bullets = []
lasers = []


def draw_bullets():
    for b in bullets:
        if -cam.x-100 < b[0][0] < -cam.x+100+W:
            pg.draw.circle(screen, (0, 0, 255),
                               (b[0][0]+cam.x, b[0][1]+cam.y), 10)


def update_bullets():
    for b in bullets:
        b[0][0] += 7 * b[1]
        b[0][1] += 7 * b[2]
        for p in players:
            if p.rect.colliderect(b[0][0]-10, b[0][1]-10, 20, 20):
                p.deaths += 1
                game_over(f"P{p.num} was pierced by a bullet")

        if COL*TS < b[0][0] < 0:
            bullets.remove(b)
        for block in collideblocks:
            if block[2] not in ["shooter", "aimbot"] and block[0].colliderect(b[0][0]-10, b[0][1]-10, 20, 20):
                if b in bullets:
                    bullets.remove(b)


player_speed = 7

if g.devmode == False:
    # intro(screen)
    main_menu(screen, game)

player1 = Player(1)
player2 = Player(2)
players: list[Player] = []
players.append(player1)
if game.players == 2:
    players.append(player2)

bg_lines = []
for i in range(22):
    i2 = i*4
    e = W/25
    x = i2*e
    bg_lines.append([[x-H, 0], [x, H]])


def draw_bg_lines():
    bg_c = bg_color
    color = (bg_c[0]+7, bg_c[1]+7, bg_c[2]+10)
    camx = cam.x*0.5
    camy = cam.y*0.5
    for l in bg_lines:
        if -camx-W-H < l[0][0]-W < -camx:
            pg.draw.line(
                screen, color, (l[0][0]+camx, l[0][1]+camy), (l[1][0]+camx, l[1][1]+camy), 40)


def addBgBlock(x, y, name):
    img = asset_manager.get_image(f"bg_blocks/{name}.png").convert()
    img.set_colorkey(BLACK)

    image = pg.transform.scale(img, (TS, TS))

    rect = image.get_rect()
    rect.topleft = x*TS, y*TS
    bg_block = [rect, image, name]
    bg_blocks.append(bg_block)


def addBlock(x, y, name, properties={}):
    img = asset_manager.get_image(f"blocks/{name}.png").convert_alpha()

    w, h = 1, 1
    if name == "moving":
        w = 2

    image = pg.transform.scale(img, (TS*w, TS*h))

    rect = image.get_rect()
    rect.topleft = x*TS, y*TS
    block = [rect, image, name, properties]
    blocks.append(block)
    if name in solid_blocks or name in ["moving", "falling", "box"]:
        collideblocks.append(block)


def loadlevel(num, reload=False):
    if reload:
        for p in players:
            p.rect.topleft = p.rpp

    if g.leveltest or g.level < g.num_of_levels + 1:
        blocks.clear()
        bullets.clear()
        collideblocks.clear()
        if not reload:
            bg_blocks.clear()
        fileName = f"assets/levels/{num}.txt"

        try:
            with open(fileName, "r") as f:
                tilemap = f.readlines()
        except Exception:
            loadlevel(1, reload)
            return

        lasers.clear()

        # place blocks
        for i, row in enumerate(tilemap):
            for j, col in enumerate(row):
                if col == ".":
                    continue

                if col == "P":
                    if not reload:
                        game.stop_player_move = True
                        for p in players:
                            p.rpp = j*TS, i*TS
                            p.rect.topleft = p.rpp

                elif col == "B":
                    addBlock(j, i, "box", {"vel_y": 0, "dx": 0})
                elif col == "G":
                    addBlock(j, i, "flag")
                elif col == "S":
                    addBlock(j, i, "spike")
                elif col == "T":
                    addBlock(j, i, "trampoline")
                elif col == "m":
                    addBlock(j, i, "moving",  {"speed": 3, "direction": 1})
                elif col == "e":
                    addBlock(j, i, "enemy",   {
                        "speed": 3, "direction": 1, "cd": 0, "frame_index": 0})
                elif col == "s":
                    addBlock(j, i, "shooter", {"cooldown": 12})

                elif col == "a":
                    addBlock(j, i, "aimbot", {"cd": 12, "d": [1, 1]})

                elif col == "-":
                    lasers.append([[j*TS, i*TS+30], [(j+1)*TS, i*TS+30]])

                elif col == "g":
                    addBlock(j, i, "grass")
                    if not reload:
                        if i > 0 and tilemap[i-1][j] == ".":
                            rn = random.random()
                            if rn < 0.1:
                                addBgBlock(j, i-1,   "grass")
                            elif rn < 0.2:
                                addBgBlock(j, i-1, "flower")
                            # elif rn < 0.3:
                            #     addBgBlock(j, i-1, "smiley")

                elif col == "d":
                    addBlock(j, i, "dirt")
                elif col == "f":
                    addBlock(j, i, "falling",    {
                        "vel_y": 0, "state": "fly", "pos": i*TS, "cd": 0})
                elif col == "c":
                    addBlock(j, i, "checkpoint", {"status": "inactive"})

    else:
        fade(screen)
        victory()


def draw_blocks():
    for b in blocks:
        if -cam.x-100 < b[0].centerx < -cam.x+100+W:
            if b[2] == "enemy":
                b[3]["cd"] += 1
                if b[3]["cd"] > 20:
                    if b[3]["frame_index"] == 0:
                        b[3]["frame_index"] = 1
                    else:
                        b[3]["frame_index"] = 0

                    i = b[3]["frame_index"] + 1
                    img = asset_manager.get_image(f"blocks/enemy/{i}.png")
                    b[1] = pg.transform.scale(img, (TS, TS))
                    b[3]["cd"] = 0

            elif b[2] == "checkpoint":
                s = b[3]["status"]
                img = asset_manager.get_image(f"blocks/checkpoint/{s}.png")
                b[1] = pg.transform.scale(img, (TS, TS))

            # elif b[2] == "aimbot":
            #    pg.draw.circle(screen, BLUE, (b[0].centerx+cam.x, b[0].centery), 500, 5)

            screen.blit(b[1], (b[0][0] + cam.x, b[0][1]+cam.y))

    for bg_b in bg_blocks:
        if -cam.x-100 < bg_b[0].centerx < -cam.x+100+W:
            screen.blit(bg_b[1], (bg_b[0][0] + cam.x, bg_b[0]
                        [1]+cam.y), special_flags=pg.BLEND_ALPHA_SDL2)


def update_blocks():
    for block in blocks:
        update_block(block)

    for block in blocks:
        if block[2] == "box":
            block[3]["dx"] = 0

def update_block(block):
    if block[2] in moving_blocks:
        atm = False
        block[0].x += block[3]["speed"] * block[3]["direction"]
        for s_block in blocks:
            if s_block != block and s_block[2] != "falling":
                if s_block[2] in solid_blocks or s_block[2] in ["enemy", "moving"]:
                    if block[0].colliderect(s_block[0]):
                        block[3]["direction"] *= -1
                    if block[2] == "enemy":
                        point = block[0].centerx+20 * \
                            block[3]["direction"], block[0].bottom+10
                        if s_block[0].collidepoint(point):
                            atm = True

        if block[2] == "enemy":
            if not atm:
                block[3]["direction"] *= -1
            for p in players:
                if block[0].colliderect(p.velrect()):
                    if p.vel_y > 1:
                        p.vel_y = -10
                        p.rotating = True
                        asset_manager.get_sound("enemy_hit.wav").play()

                        if block in blocks:
                            blocks.remove(block)
                    else:
                        p.alive = False

    elif block[2] == "shooter":
        block[3]["cooldown"] -= 1
        if block[3]["cooldown"] <= 0 and (-cam.x-100 < block[0].centerx < -cam.x+100+W):
            bullets.append([[block[0].centerx, block[0].centery],  1, 0])
            bullets.append([[block[0].centerx, block[0].centery], -1, 0])
            block[3]["cooldown"] = 120
            asset_manager.get_sound("shoot.wav").play()

    elif block[2] == "aimbot":
        block[3]["cd"] -= 1
        if block[3]["cd"] <= 0:
            r = block[0]
            target = choice(players).rect
            if hypot(target.centery-r.centery, target.centerx-r.centerx) < 500:

                lineclip = False
                for b in collideblocks:
                    if b[0].clipline((target.centerx, target.centery), (block[0].centerx, block[0].centery)):
                        lineclip = True

                if not lineclip:
                    radians = atan2(r.centery-target.centery,
                                    r.centerx-target.centerx)

                    dx, dy = cos(radians), sin(radians)

                    bullets.append([[r.centerx, r.centery], -dx, -dy])
                    block[3]["cd"] = 70
                    asset_manager.get_sound("shoot.wav").play()

    elif block[2] == "falling":
        if block[3]["state"] == "fall":
            if block[3]["cd"] > 0:
                block[3]["cd"] -= 1
            else:
                block[3]["vel_y"] += GRAVITY
                block[0].y += block[3]["vel_y"]
                if block[0].y > block[3]["pos"]+1500:
                    block[3]["state"] = "fly"

        elif block[3]["state"] == "fly":
            block[3]["cd"] = 12
            block[3]["vel_y"] = 0
            block[0].y = block[3]["pos"]

    elif block[2] == "trampoline":
        for p in players:
            if p.vel_y > 1:
                if pg.Rect(p.rect.x, p.rect.y + p.vel_y, p.rect.width, p.rect.height).colliderect(
                        block[0].x, block[0].y + (TS * 0.4), block[0].width, block[0].height - (TS * 0.4)):

                    p.vel_y = TRAMPOLINE_VEL
                    asset_manager.get_sound("trampoline.wav").play()

                    p.rotating = True

    elif block[2] == "checkpoint":
        if block[3]["status"] == "inactive":
            for p in players:
                if p.rect.colliderect(block[0]):
                    asset_manager.get_sound("checkpoint.wav").play()
                    block[3]["status"] = "active"
                    for player in players:
                        player.rpp = block[0].x, block[0].y

    elif block[2] == "box":
        block[3]["vel_y"] += GRAVITY
        for col_b in blocks:
            if block == col_b:
                continue

            rect = pg.Rect(block[0].x, block[0].y + block[3]["vel_y"], TS, TS)
            if not col_b[0].colliderect(rect):
                continue

            if col_b[2] == "enemy" and block[3]["vel_y"] > 2:
                block[3]["vel_y"] = -6
                asset_manager.get_sound("enemy_hit.wav").play()
                if col_b in blocks:
                    blocks.remove(col_b)

            elif col_b[2] in solid_blocks:
                # if col_b[2] == "box":
                #     block[3]["dx"] == col_b[3]["dx"]
                #     update_block(col_b)
                block[3]["vel_y"] = 0

            elif col_b[2] == "trampoline":
                block[3]["vel_y"] = TRAMPOLINE_VEL

        for p in players:
            rect = pg.Rect(block[0].x, block[0].y + block[3]["vel_y"], TS, TS)
            if p.rect.colliderect(rect) and block[3]["vel_y"] > 2:
                block[3]["vel_y"] = -6
                asset_manager.get_sound("enemy_hit.wav").play()
                p.deaths += 1
                p.explode()
                game_over(f"P{p.num} was crushed by a box.")

        block[0].y += block[3]["vel_y"]
        block[0].x += block[3]["dx"]
        # block[3]["dx"] = 0

    elif block[2] == "flag":
        if g.players == 1:
            collision = block[0].colliderect(player1.rect)

        else:
            collision = block[0].colliderect(
                player1.rect) and block[0].colliderect(player2.rect)

        if collision:
            asset_manager.get_sound("level_completed.wav").play()
            game.level += 1

            if game.level > data["completed_lvls"]:
                data["completed_lvls"] = game.level
                with open("data.json", "r+") as f:
                    json.dump(data, f)

            game.stop_player_move = True
            loadlevel(game.level)
            fade(screen)

    elif block[2] == "spike":
        for p in players:
            if p.vel_y >= 2:
                if p.velrect().colliderect(
                        block[0].x, block[0].y + (block[0].height / 2), block[0].width, block[0].height / 2):
                    p.deaths += 1
                    p.explode()
                    game_over(f"P{p.num} jumped into a spike")


def draw_players():
    player1.draw()
    if game.players == 2:
        player2.draw()


def player_updates():
    player1.move(left, right)
    player1.update()

    if game.players == 2:
        player2.move(left2, right2)
        player2.update()


def update_lasers():
    for l in lasers:
        for p in players:
            if p.rect.clipline(l):
                asset_manager.get_sound("laser.wav").play()
                p.explode()
                p.deaths += 1
                cause = choice(["was cut apart", "can\"t jump big enough"])
                game_over(f"P{p.num} {cause}")

def draw_lasers():
    for l in lasers:
        pg.draw.line(
            screen,
            RED,
            (l[0][0]+cam.x, l[0][1]+cam.y),
            (l[1][0]+cam.x, l[1][1]+cam.y),
            5
        )

def reDraw():
    screen.fill(bg_color)

    draw_bg_lines()

    draw_blocks()
    draw_players()
    draw_bullets()
    draw_lasers()

    stats_display()

    pg.display.update()


game.color_selection()
level_selection(screen, game)
loadlevel(game.level)

should_pause = False
run = True
while run:
    if not vsync:
        clock.tick(FPS)

    reDraw()

    if game.stop_player_move:
        left,  right = False, False
        left2, right2 = False, False
        for p in players:
            p.vel_y = 0
            p.jump = False
            p.knockback = 0
        game.stop_player_move = False

    player_updates()
    update_lasers()
    update_blocks()
    cam.update()
    update_bullets()

    if should_pause:
        game.stop_player_move = True
        game.loadlevel_bool = False
        pause(screen, game)
        if game.loadlevel_bool:
            level_selection(screen, game)
            if game.level_selected:
                loadlevel(game.level)
                game.loadlevel_bool = False
        should_pause = False

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN:

            if event.key == pg.K_k:
                fly = not fly

            if event.key == pg.K_KP_0:
                p = player2
                j = p.rect.x/TS
                i = p.rect.y/TS+1.3
                # addBlock(p.rect.x/TS, p.rect.y/TS+1, "box", {"vel_y": -20})
                # addBlock(j, i, "falling",    {"vel_y": 0, "state": "fly", "pos": i*TS, "cd": 0})
                addBlock(j, i, "enemy",   {
                         "speed": 1, "direction": 1, "cd": 0, "frame_index": 0})

            if event.key == pg.K_r:
                reload = not event.mod & pg.KMOD_LSHIFT
                loadlevel(g.level, reload)

            if event.key == pg.K_F2:
                screenshot()
                should_pause = True

            if event.key in [pg.K_ESCAPE, pg.K_SPACE]:
                should_pause = True

            if event.key == pg.K_F11:
                fullscreen = not fullscreen
                pg.display.toggle_fullscreen()

            # player 1
            if event.key == pg.K_w:
                player1.jump = True
            if event.key == pg.K_a:
                left = True
            if event.key == pg.K_d:
                right = True

            # player 2
            if event.key == pg.K_UP:
                player2.jump = True
            if event.key == pg.K_RIGHT:
                right2 = True
            if event.key == pg.K_LEFT:
                left2 = True

        if event.type == pg.KEYUP:
            # player 1
            if event.key == pg.K_w:
                player1.jump = False
            if event.key == pg.K_a:
                left = False
            if event.key == pg.K_d:
                right = False

            # player 2
            if game.players == 2:
                if event.key == pg.K_UP:
                    player2.jump = False
                if event.key == pg.K_RIGHT:
                    right2 = False
                if event.key == pg.K_LEFT:
                    left2 = False

pg.quit()
sys.exit()

