import random
import pygame as pg
import json
import sys
from math import sin, cos, atan2, hypot

from scripts.level_selection import level_selection
from scripts.main_menu import main_menu
from scripts import consts, button, util
from scripts.assets import asset_manager

with open("config.json", "r") as f:
    config = json.load(f)
    fullscreen = config["auto_fullscreen"]
    vsync = config["vsync"]

screen = pg.display.set_mode((consts.W, consts.H), vsync=vsync)
pg.display.set_caption("SuperMuki")

asset_manager.load_player_imgs("player")


class Game:
    def __init__(self):
        self.gui_rgb = (0, 0, 80)
        self.num_of_levels = 10
        self.level = 1
        self.load_level_bool = False
        self.level_selected = False

        self.players = 1
        self.stop_player_move = False
        self.respawn_point = (0.0, 0.0)

        self.flip_when_jump = True
        self.show_deaths = True

        self.flying = False

    def main_menu(self):
        n = menu.main_menu(screen)
        # n = len(config.controls)
        self.players = [Player(i + 1) for i in range(n)]

    def pause(self):
        for player in self.players:
            player.stop()

        ret = menu.pause_menu(screen)
        if ret == menu.code.LEVEL_SELECT:
            level = menu.level_selection(screen)
            load_level(level)

        elif ret == menu.code.MAIN_MENU:
            self.main_menu()

            for player in self.players:
                player.deaths = 0

            self.color_selection()
            level = menu.level_selection(screen)
            load_level(level)

        elif ret == menu.code.COLOR_SELECT:
            self.color_selection()

    def color_selection(self):
        colors = [p.color for p in self.players]
        menu.color_selection(screen, colors)
        for player in self.players:
            print(player.color)
            player.images = util.recolor_player(player.color)


def draw_stats():
    util.draw_text(screen, False, 30, f"level {game.level}", "white", 15, 15)

    if game.flying:
        util.draw_text(screen, True, 20, "fly", "white", consts.CX, 30)

    if game.show_deaths:
        util.draw_text(screen, True, 30, "deaths", "white", consts.W - 80, 30)
        if game.players == 1:
            util.draw_text(
                screen, True, 30, f"{player1.deaths}",
                player1.color, consts.W - 80, 90
            )

        elif game.players == 2:
            for player in players:
                util.draw_text(
                    screen, True, 30, f"{player.deaths}",
                    player.color, consts.W-200+(80*player.num), 90
                )


class Camera:
    def __init__(self):
        self.x = 0
        self.target_x = 0
        self.float_x = 0

        self.y = 0
        self.target_y = 0
        self.float_y = 0

        self.preferred: Player | None = None

    def update(self):
        if game.players == 2:
            self.target_x = - (
                player1.rect.centerx + player2.rect.centerx
            ) / 2 + consts.CX

            distance = abs(player1.rect.centerx - player2.rect.centerx)
            far_apart = distance > consts.W - 300

            if far_apart and self.preferred:
                self.target_x = -self.preferred.rect.centerx + consts.CX

            # self.target_y = -(
            #     (player1.rect.centery + player2.rect.centery) / 2
            # ) + consts.CY

        elif game.players == 1:
            self.target_x = -player1.rect.centerx + consts.CX
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
        self.speed = consts.PLAYER_SPEED
        self.knockback = 0
        self.jump = False
        self.vel_y = 0

        # - alive
        self.alive = True
        self.deaths = 0

    def update(self):
        self.flip = (self.direction == -1)

        if self.rect.bottom > consts.ROW*consts.TS and self.alive:
            self.kill()
            self.rect.bottom = consts.ROW * consts.TS

        if self.rect.top > consts.ROW*consts.TS and not self.alive:
            self.respawn()

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > 6000:
            self.rect.right = 6000

    def move(self, left, right):
        dx = 0
        dy = 0

        if self.alive and left and not right:
            cam.preferred = self
            dx = -self.speed
            self.direction = -1

        if self.alive and right and not left:
            cam.preferred = self
            dx = self.speed
            self.direction = 1

        if self.jump and (game.flying or self.atj):
            self.vel_y = -10
            self.rotating = True
            # print("e")
            self.jump = False

        if left or right and self.atj:
            self.animation_cd += 1
            if self.animation_cd >= 7:
                e = {1: 2, 2: 1, 3: 1}
                self.frame_index = e[self.frame_index]
                self.animation_cd = 0
        else:
            self.frame_index = 3

        if (self.rotating and game.flip_when_jump) or not self.alive:
            self.rotation -= 15
            # print("rotating")
            if abs(self.rotation) > 355:
                self.rotation = 0
                self.rotating = False

        dy += self.vel_y
        dx += self.knockback
        now_on_ground = False

        for block in collideblocks:
            if not self.alive:
                break

            if block[2] == "moving":
                if block[0].colliderect(
                    self.rect.x + dx, self.rect.y + dy + 10,
                    self.rect.width, self.rect.height
                ) and self.vel_y > -1:
                    if self.vel_y > 0:
                        self.vel_y = 0
                        self.atj = True
                        now_on_ground = True
                        dy = block[0].top - self.rect.bottom

                    dx = block[3]["speed"] * block[3]["direction"]

            if block[2] in solid_blocks:
                if block[0].colliderect(
                    self.rect.x + dx, self.rect.y,
                    self.rect.width, self.rect.height
                ):
                    if block[2] == "box":  # and self.atj:
                        dx = int(dx*0.3)
                        x_collide = False
                        for col_block in blocks:
                            if col_block != block:
                                if col_block[0].colliderect(
                                    block[0][0] + dx, block[0][1],
                                    consts.TS, consts.TS
                                ) or block[0].x < 0:
                                    x_collide = True

                        if x_collide:
                            dx = 0
                        # block[0].x += dx
                        block[3]["dx"] += dx

                    else:
                        dx = 0
                    self.knockback = 0
                if block[0].colliderect(
                    self.rect.x, self.rect.y + dy,
                    self.rect.width, self.rect.height
                ):
                    # if self.vel_y <= 0:
                    if block[0].bottom < self.rect.bottom:
                        self.vel_y = 0
                        dy = block[0].bottom - self.rect.top
                        if self.atj and self.alive:
                            self.kill()

                    else:
                        if block[2] == "falling":
                            block[3]["state"] = "fall"

                        self.vel_y = 0
                        now_on_ground = True
                        self.atj = True
                        dy = block[0].top - self.rect.bottom
                        self.rotating = False
                        self.rotation = 0

                    # cam.x += 300

        if abs(self.vel_y) >= 5:
            self.atj = False

        self.rect.x += dx
        self.rect.y += dy

        if not now_on_ground:
            self.vel_y += consts.GRAVITY

    def kill(self):
        if not self.alive:
            return

        asset_manager.get_sound("enemy_hit.wav").play()
        self.alive = False
        self.vel_y = -12

    def respawn(self):
        self.alive = True
        self.rotating = False
        self.rotation = 0
        self.vel_y = 0
        self.rect.topleft = game.respawn_point

    def velrect(self):
        return pg.Rect(
            self.rect.x, self.rect.y + self.vel_y,
            self.rect.width, self.rect.height
        )

    def draw(self):
        c_img = self.images[self.frame_index-1]
        if self.rect.bottom < 0:
            fallpos_image = c_img.copy()
            fallpos_image.set_alpha(80)
            screen.blit(
                pg.transform.flip(fallpos_image, self.flip, False),
                (self.rect.x + cam.x, 30)
            )

        if game.flip_when_jump:
            img_to_blit = pg.transform.rotate(c_img, self.rotation)

        else:
            img_to_blit = c_img

        # screen.blit(flip(img_to_blit, self.flip),
        #             (self.rect.x+cam.x, self.rect.y+cam.y))

        flipped = pg.transform.flip(img_to_blit, self.flip, False)

        # if not self.alive:
        #     flipped = flip_ver(flipped, True)

        rect = flipped.get_rect()
        rect.centerx = self.rect.centerx + cam.x
        rect.centery = self.rect.centery + cam.y
        screen.blit(flipped, rect)


solid_blocks = ["grass", "dirt", "shooter", "box", "falling"]
moving_blocks = ["moving", "enemy"]

collideblocks = []
reset_blocks = []

blocks = []
bg_blocks = []
bullets = []
lasers = []


def draw_bullets():
    for b in bullets:
        if -cam.x-100 < b[0][0] < -cam.x+100+consts.W:
            pg.draw.circle(screen, (0, 0, 255),
                           (b[0][0]+cam.x, b[0][1]+cam.y), 10)


def update_bullets():
    for b in bullets:
        b[0][0] += 7 * b[1]
        b[0][1] += 7 * b[2]
        for p in players:
            if p.rect.colliderect(b[0][0]-10, b[0][1]-10, 20, 20):
                p.kill()
                # p.deaths += 1
                # game_over(f"P{p.num} was pierced by a bullet")

        if consts.COL*consts.TS < b[0][0] < 0:
            bullets.remove(b)
        for block in collideblocks:
            if (
                block[2] not in ["shooter", "aimbot"] and
                block[0].colliderect(b[0][0]-10, b[0][1]-10, 20, 20)
            ):
                if b in bullets:
                    bullets.remove(b)


main_menu(screen, game)

player1 = Player(1)
player2 = Player(2)
players = [player1]
if game.players == 2:
    players.append(player2)

bg_lines = []
for i in range(22):
    i2 = i*4
    e = consts.W/25
    x = i2*e
    bg_lines.append([[x-consts.H, 0], [x, consts.H]])


def draw_bg_lines():
    bg_c = consts.bg_color
    color = (bg_c[0]+7, bg_c[1]+7, bg_c[2]+10)
    camx = cam.x*0.5
    camy = cam.y*0.5
    for line in bg_lines:
        if -camx-consts.W-consts.H < line[0][0]-consts.W < -camx:
            pg.draw.line(
                screen, color,
                (line[0][0]+camx, line[0][1]+camy),
                (line[1][0]+camx, line[1][1]+camy),
                40
            )


def add_block(x, y, name, properties={}):
    img = asset_manager.get_image(f"blocks/{name}.png").convert_alpha()

    h = 1
    w = 2 if name == "moving" else 1

    image = pg.transform.scale(img, (consts.TS*w, consts.TS*h))

    rect = image.get_rect()
    rect.topleft = x*consts.TS, y*consts.TS
    block = [rect, image, name, properties]
    blocks.append(block)

    if name in solid_blocks or name in ["moving", "falling", "box"]:
        collideblocks.append(block)


def load_level(num, reload=False):
    if reload:
        for p in players:
            p.rect.topleft = game.respawn_point

    if not exists(file_name):
        level = menu.level_selection(screen)
        load_level(level)
        return

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
        load_level(1, reload)
        return

    lasers.clear()

    # place blocks
    for i, row in enumerate(tilemap):
        for j, col in enumerate(row):
            if col == ".":
                continue

            if col == "P" and not reload:
                game.stop_player_move = True
                game.respawn_point = j*consts.TS, i*consts.TS
                for p in players:
                    p.rect.topleft = game.respawn_point

            elif col == "B":
                add_block(j, i, "box", {"vel_y": 0, "dx": 0})
            elif col == "G":
                add_block(j, i, "flag")
            elif col == "S":
                add_block(j, i, "spike")
            elif col == "T":
                add_block(j, i, "trampoline")
            elif col == "m":
                add_block(j, i, "moving",  {"speed": 3, "direction": 1})
            elif col == "e":
                add_block(j, i, "enemy", {
                    "speed": 3,
                    "direction": 1,
                    "cd": 0,
                    "frame_index": 0
                })
            elif col == "s":
                add_block(j, i, "shooter", {"cooldown": 12})

            elif col == "a":
                add_block(j, i, "aimbot", {"cd": 12, "d": [1, 1]})

            elif col == "-":
                lasers.append([
                    [j*consts.TS, i*consts.TS+30],
                    [(j+1)*consts.TS, i*consts.TS+30]
                ])

            elif col == "g":
                add_block(j, i, "grass")
            elif col == "d":
                add_block(j, i, "dirt")
            elif col == "f":
                add_block(j, i, "falling", {
                    "vel_y": 0,
                    "state": "fly",
                    "pos": i*consts.TS,
                    "cd": 0
                })
            elif col == "c":
                add_block(j, i, "checkpoint", {"status": "inactive"})


def draw_blocks():
    def on_screen(x):
        return -cam.x - 100 < x < -cam.x + 100 + consts.W

    for b in blocks:
        if not on_screen(b[0].centerx):
            continue

        if b[2] == "enemy":
            b[3]["cd"] += 1
            if b[3]["cd"] > 20:
                if b[3]["frame_index"] == 0:
                    b[3]["frame_index"] = 1
                else:
                    b[3]["frame_index"] = 0

                i = b[3]["frame_index"] + 1
                img = asset_manager.get_image(f"blocks/enemy/{i}.png")
                b[1] = pg.transform.scale(img, (consts.TS, consts.TS))
                b[3]["cd"] = 0

        elif b[2] == "checkpoint":
            s = b[3]["status"]
            img = asset_manager.get_image(f"blocks/checkpoint/{s}.png")
            b[1] = pg.transform.scale(img, (consts.TS, consts.TS))

        screen.blit(b[1], (b[0][0] + cam.x, b[0][1]+cam.y))

    for bg_b in bg_blocks:
        if not on_screen(bg_b[0].centerx):
            continue

        screen.blit(
            bg_b[1],
            (bg_b[0][0] + cam.x, bg_b[0][1]+cam.y),
            special_flags=pg.BLEND_ALPHA_SDL2
        )


def update_blocks():
    for block in blocks:
        update_block(block)

    for block in blocks:
        if block[2] == "box":
            block[3]["dx"] = 0


def update_block(block):
    rect, _, name, props = block
    if name in moving_blocks:
        # can the enemy walk forward (able to move)
        atm = False
        rect.x += props["speed"] * props["direction"]
        for s_block in blocks:
            if (
                s_block == block or
                s_block[2] not in (solid_blocks + ["enemy", "moving"]) or
                s_block[2] == "falling"
            ):
                continue

            if rect.colliderect(s_block[0]):
                props["direction"] *= -1

            if name == "enemy":
                if s_block[0].collidepoint(
                    rect.centerx + 20*props["direction"],
                    rect.bottom + 10
                ):
                    atm = True

        if name == "enemy":
            if not atm:
                props["direction"] *= -1

            for p in players:
                if not (p.alive and rect.colliderect(p.velrect())):
                    continue

                if p.vel_y > 1:
                    p.vel_y = -10
                    p.rotating = True
                    asset_manager.get_sound("enemy_hit.wav").play()

                    if block in blocks:
                        blocks.remove(block)

                else:
                    p.kill()

    elif name == "shooter":
        props["cooldown"] -= 1

        if (
            props["cooldown"] <= 0 and
            (-cam.x-100 < rect.centerx < -cam.x+100+consts.W)
        ):
            bullets.append([list(rect.center),  1, 0])
            bullets.append([list(rect.center), -1, 0])
            props["cooldown"] = 120
            asset_manager.get_sound("shoot.wav").play()

    elif name == "aimbot":
        props["cd"] -= 1
        if props["cd"] > 0:
            return

        alive_players = [ p for p in players if p.alive ]

        if not alive_players:
            return

        target = random.choice(alive_players).rect

        dx = target.centerx - rect.centerx
        dy = target.centery - rect.centery
        dist = hypot(dx, dy)

        if not 0 < dist < 500:
            return

        for b in collideblocks:
            if b[0].clipline(target.center, rect.center):
                return

        vx = dx / dist
        vy = dy / dist

        bullets.append([list(rect.center), vx, vy])
        props["cd"] = 70
        asset_manager.get_sound("shoot.wav").play()

    elif name == "falling":
        if props["state"] == "fall":
            if props["cd"] > 0:
                props["cd"] -= 1
            else:
                props["vel_y"] += consts.GRAVITY
                rect.y += props["vel_y"]
                if rect.y > props["pos"] + 1500:
                    props["state"] = "fly"

        elif props["state"] == "fly":
            props["cd"] = 12
            props["vel_y"] = 0
            rect.y = props["pos"]

    elif name == "trampoline":
        for p in players:
            if not p.alive or p.vel_y < 1:
                continue

            p_rect = pg.Rect(
                p.rect.x, p.rect.y + p.vel_y,
                p.rect.width, p.rect.height
            )

            block_hitbox = pg.Rect(
                rect.x, rect.y + (consts.TS * 0.4),
                rect.width, rect.height - (consts.TS * 0.4)
            )

            if p_rect.colliderect(block_hitbox):
                p.vel_y = consts.TRAMPOLINE_VEL
                asset_manager.get_sound("trampoline.wav").play()
                p.rotating = True

    elif name == "checkpoint":
        if props["status"] == "active":
            return

        for p in players:
            if not p.rect.colliderect(rect):
                continue

            asset_manager.get_sound("checkpoint.wav").play()
            props["status"] = "active"
            game.respawn_point = rect.topleft

    elif name == "box":
        props["vel_y"] += consts.GRAVITY
        for col_b in blocks:
            if block == col_b or not col_b[0].colliderect(
                rect.x,
                rect.y + props["vel_y"],
                consts.TS,
                consts.TS
            ):
                continue

            if col_b[2] == "enemy" and props["vel_y"] > 2:
                props["vel_y"] = -6
                asset_manager.get_sound("enemy_hit.wav").play()
                if col_b in blocks:
                    blocks.remove(col_b)

            elif col_b[2] in solid_blocks:
                # if col_b[2] == "box":
                #     block[3]["dx"] == col_b[3]["dx"]
                #     update_block(col_b)
                props["vel_y"] = 0

            elif col_b[2] == "trampoline":
                props["vel_y"] = consts.TRAMPOLINE_VEL

        for player in players:
            if not player.alive or props["vel_y"] < 2:
                continue

            if player.rect.colliderect(
                rect.x,
                rect.y + props["vel_y"],
                consts.TS,
                consts.TS
            ):
                props["vel_y"] = -6
                player.kill()

        rect.y += props["vel_y"]
        rect.x += props["dx"]
        # block[3]["dx"] = 0

    elif name == "flag":
        collision = rect.colliderect(player1.rect)

        if game.players == 2:
            collision &= rect.colliderect(player2.rect)

        if collision:
            asset_manager.get_sound("level_completed.wav").play()
            game.level += 1

            game.stop_player_move = True
            load_level(game.level)

    elif name == "spike":
        for player in players:
            if not player.alive or player.vel_y < 2:
                continue

            if player.velrect().colliderect(
                rect.x,
                rect.y + (rect.height / 2),
                rect.width,
                rect.height / 2
            ):
                player.kill()
                # p.deaths += 1
                # p.explode()
                # game_over(f"P{p.num} jumped into a spike")


def draw():
    screen.fill(consts.GAME_BG_COLOR)

    draw_bg_lines()

    for block in blocks:
        draw_block(block)

    for player in game.players:
        player.draw()

    for bullet in bullets:
        if not - consts.BULLET_R < bullet[0].x + game.camera.x < consts.BULLET_R + consts.W:
            continue

        pos = (bullet[0].x + game.camera.x, bullet[0].y)
        pg.draw.circle(screen, "blue", pos, consts.BULLET_R)

    for laser in lasers:
        pg.draw.line(
            screen,
            "red",
            (laser[0][0] + game.camera.x, laser[0][1] + game.camera.y),
            (laser[1][0] + game.camera.x, laser[1][1] + game.camera.y),
            5,
        )

    draw_stats()

    pg.display.update()


def update():
    for player in game.players:
        player.move()
        player.update()

    for laser in lasers:
        for player in game.players:
            if player.alive and player.rect.clipline(laser):
                player.kill()

    for block in blocks:
        update_block(block)

    for bullet in bullets:
        update_bullet(bullet)

    game.camera.update()


def handle_events():
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            util.close()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_k:
                # print(len(collideblocks) / len(blocks))
                game.flying = not game.flying

            elif event.key == pg.K_r:
                reload = not event.mod & pg.KMOD_LSHIFT
                load_level(reload=reload)

            elif event.key == pg.K_F2:
                util.screenshot()
                game.pause()

            elif event.key in [pg.K_ESCAPE, pg.K_SPACE]:
                game.pause()

            elif event.key == pg.K_F11:
                config.fullscreen = not config.fullscreen
                pg.display.toggle_fullscreen()

        if event.type in [pg.KEYDOWN, pg.KEYUP]:
            down = event.type == pg.KEYDOWN

            for p, c in zip(game.players, config.controls):
                if event.key == c[0]:
                    p.left = down
                elif event.key == c[1]:
                    p.right = down
                elif event.key == c[2]:
                    p.jump = down


if __name__ == "__main__":
    screen = pg.display.set_mode((consts.W, consts.H), vsync=config.vsync)
    pg.display.set_caption("SuperMuki")

    asset_manager.load_player_imgs()
    asset_manager.set_audio_volume(config.audio_volume)
    solid_blocks = ["grass", "dirt", "shooter", "falling", "moving", "box", "enemy"]
    moving_blocks = ["moving", "enemy"]

    blocks = []
    bullets = []
    lasers = []

    bg_lines = []
    for i in range(22):
        x = i * 4 * consts.W / 25
        bg_lines.append([[x - consts.H, 0], [x, consts.H]])

    game = Game()
    game.main_menu()
    game.color_selection()
    level = menu.level_selection(screen)
    load_level(1 if level is None else level)

    while True:
        if not config.vsync:
            consts.clock.tick(consts.FPS)

        handle_events()
        update()
        draw()

