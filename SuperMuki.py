import random
import os
from math import hypot

import pygame as pg
from pygame import Vector2 as Vec

from scripts import consts, util, menu
from scripts.assets import asset_manager
import config


class Game:
    def __init__(self):
        self.current_level = 1

        self.players: list[Player] = []
        self.camera = Camera()
        self.respawn_point = (0.0, 0.0)

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
    util.draw_text(screen, False, 30, f"level {game.current_level}", "white", 15, 15)

    if game.flying:
        util.draw_text(screen, True, 20, "fly", "white", consts.CX, 30)

    if config.show_deaths:
        util.draw_text(screen, True, 30, "deaths", "white", consts.W - 80, 30)
        for player in game.players:
            util.draw_text(
                screen,
                True,
                30,
                f"{player.deaths}",
                player.color,
                consts.W - 200 + (80 * player.num),
                90,
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

    def on_screen(self, rect: pg.Rect) -> bool:
        return -self.x < rect.right and rect.left < -self.x + 100 + consts.W

    def update(self):
        p1 = game.players[0]
        p2 = game.players[1] if len(game.players) >= 2 else None
        if p2 is not None:
            self.target_x = (
                -(p1.rect.centerx + p2.rect.centerx) / 2 + consts.CX
            )

            distance = abs(p1.rect.centerx - p2.rect.centerx)
            far_apart = distance > consts.W - 300

            if far_apart and self.preferred:
                self.target_x = -self.preferred.rect.centerx + consts.CX

            # self.target_y = -(
            #     (player1.rect.centery + player2.rect.centery) / 2
            # ) + consts.CY

        else:
            self.target_x = -p1.rect.centerx + consts.CX
            # self.target_y = -player1.rect.centery + CY

        self.float_x += (self.target_x - self.float_x) * 0.05
        self.x = int(self.float_x)

        self.float_y += (self.target_y - self.float_y) * 0.05
        self.y = int(self.float_y)

        if self.x > 0:
            self.x = 0

        if self.x < -4720:
            self.x = -4720




class Player:
    def __init__(self, num):
        # graphical -----
        self.color = [255, 0, 0]
        self.flip = False
        self.rotation = 0
        self.rotating = False

        self.frame_index = 1
        self.animation_cd = 0
        self.images = util.recolor_player(self.color)

        # logical -------
        self.num = num
        self.able_to_jump = False
        self.rect: pg.Rect = self.images[0].get_rect()
        self.direction = 1

        # - movement ----
        self.speed = consts.PLAYER_SPEED
        self.knockback = 0
        self.vel_y = 0
        # -- controls ---
        self.jump = False
        self.left = False
        self.right = False

        # - alive
        self.alive = True
        self.deaths = 0

    def update(self):
        self.flip = self.direction == -1

        if self.left or self.right and self.able_to_jump:
            self.animation_cd += 1
            if self.animation_cd >= 7:
                self.frame_index = 2 if self.frame_index == 1 else 1
                self.animation_cd = 0
        else:
            self.frame_index = 3

        if (self.rotating and config.flip_when_jump) or not self.alive:
            self.rotation -= 15
            # print("rotating")
            if abs(self.rotation) > 355:
                self.rotation = 0
                self.rotating = False

        if self.rect.bottom > consts.ROW * consts.TS and self.alive:
            self.kill()
            self.rect.bottom = consts.ROW * consts.TS

        if self.rect.top > consts.ROW * consts.TS and not self.alive:
            self.respawn()

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > 6000:
            self.rect.right = 6000

    def move(self):
        dx = 0
        dy = 0

        self.vel_y += consts.GRAVITY

        movement_dir = self.right - self.left
        if self.alive and movement_dir != 0:
            game.camera.preferred = self
            dx = movement_dir * self.speed
            self.direction = movement_dir

        if self.alive and self.jump and (game.flying or self.able_to_jump):
            self.vel_y = consts.JUMP_VEL
            self.rotating = True
            self.jump = False

        dy += self.vel_y
        dx += self.knockback

        for block in blocks:
            if not self.alive:
                break

            b_rect, _, b_name, b_props = block

            if b_name not in consts.SOLID_BLOCKS:
                continue

            if b_name == "moving":
                if (
                    b_rect.colliderect(
                        self.rect.x + dx,
                        self.rect.y + dy + 10,
                        self.rect.width,
                        self.rect.height,
                    )
                    and self.vel_y > -1
                ):
                    if self.vel_y > 0:
                        self.vel_y = 0
                        self.able_to_jump = True
                        dy = b_rect.top - self.rect.bottom

                    dx = b_props["speed"] * b_props["direction"]

            if b_rect.colliderect(
                (self.rect.x + dx, self.rect.y),
                (self.rect.width, self.rect.height),
            ):
                self.knockback = 0
                if not (b_name == "box" and self.able_to_jump):
                    dx = 0
                    continue

                dx = int(dx * 0.3)
                x_collide = False
                for col_block in blocks:
                    if col_block == block:
                        continue

                    if (
                        col_block[0].colliderect(
                            b_rect.x + dx,
                            b_rect.y,
                            consts.TS,
                            consts.TS,
                        )
                        or b_rect.x < 0
                    ):
                        x_collide = True

                if x_collide:
                    dx = 0

                b_props["dx"] += dx

            if b_rect.colliderect(
                (self.rect.x, self.rect.y + dy),
                (self.rect.width, self.rect.height),
            ):
                # if self.vel_y <= 0:
                if b_rect.bottom < self.rect.bottom:
                    self.vel_y = 0
                    dy = b_rect.bottom - self.rect.top
                    if self.able_to_jump and self.alive:
                        self.kill()

                else:
                    if b_name == "falling":
                        b_props["state"] = "fall"

                    self.vel_y = 0
                    self.able_to_jump = True
                    dy = b_rect.top - self.rect.bottom
                    self.rotating = False
                    self.rotation = 0

        if abs(self.vel_y) >= 5:
            self.able_to_jump = False

        self.rect.x += dx
        self.rect.y += dy

    def stop(self):
        self.vel_y = 0
        self.jump = False
        self.left = False
        self.right = False
        self.knockback = 0

    def kill(self):
        if not self.alive:
            return

        asset_manager.play_sound("enemy_hit.wav")
        self.alive = False
        self.vel_y = -12
        self.deaths += 1

    def respawn(self):
        self.alive = True
        self.rotating = False
        self.rotation = 0
        self.vel_y = 0
        self.rect.topleft = game.respawn_point

    def velrect(self):
        return pg.Rect(
            (self.rect.x, self.rect.y + self.vel_y),
            (self.rect.width, self.rect.height),
        )

    def draw(self):
        c_img = self.images[self.frame_index - 1]

        if self.rect.bottom < 0:
            fallpos_image = c_img.copy()
            fallpos_image.set_alpha(80)
            screen.blit(
                pg.transform.flip(fallpos_image, self.flip, False),
                (self.rect.x + game.camera.x, 30),
            )
            return

        if config.flip_when_jump:
            img_to_blit = pg.transform.rotate(c_img, self.rotation)

        else:
            img_to_blit = c_img

        # screen.blit(flip(img_to_blit, self.flip),
        #             (self.rect.x+cam.x, self.rect.y+cam.y))

        flipped = pg.transform.flip(img_to_blit, self.flip, False)

        # if not self.alive:
        #     flipped = flip_ver(flipped, True)

        rect = flipped.get_rect()
        rect.centerx = self.rect.centerx + game.camera.x
        rect.centery = self.rect.centery + game.camera.y
        screen.blit(flipped, rect)


def update_bullet(bullet: list[Vec]):
    bullet[0] += 7 * bullet[1]
    bullet_rect = pg.Rect(bullet[0].x - 10, bullet[0].y - 10, 20, 20)

    for player in game.players:
        if player.rect.colliderect(bullet_rect):
            player.kill()

    if consts.COL * consts.TS < bullet[0].x < 0:
        bullets.remove(bullet)
        return

    for block in blocks:
        if block[2] in ["aimbot", "shooter"]:
            continue

        if block[0].colliderect(bullet_rect):
            bullets.remove(bullet)
            return


def draw_bg_lines():
    color = (
        consts.GAME_BG_COLOR[0] + 4,
        consts.GAME_BG_COLOR[1] + 4,
        consts.GAME_BG_COLOR[2] + 7,
    )
    camx = game.camera.x * 0.5
    camy = game.camera.y * 0.5
    for line in bg_lines:
        if -camx - consts.W - consts.H < line[0][0] - consts.W < -camx:
            pg.draw.line(
                screen,
                color,
                (line[0][0] + camx, line[0][1] + camy),
                (line[1][0] + camx, line[1][1] + camy),
                40,
            )


def add_block(x, y, name, properties={}):
    img = asset_manager.get_image(f"blocks/{name}.png").convert_alpha()

    w = 2 if name == "moving" else 1
    image = pg.transform.scale(img, (consts.TS * w, consts.TS))

    rect = image.get_rect()
    rect.topleft = x * consts.TS, y * consts.TS
    block = [rect, image, name, properties]
    blocks.append(block)


def load_level(num: int | None = None, reload=False):
    if num is not None:
        game.current_level = num

    file_name = f"assets/levels/{game.current_level}.txt"

    if not os.path.exists(file_name):
        level = menu.level_selection(screen)
        load_level(level)
        return

    with open(file_name, "r") as f:
        tilemap = f.readlines()

    for player in game.players:
        if reload:
            player.rect.topleft = game.respawn_point
        else:
            player.deaths = 0

    blocks.clear()
    bullets.clear()
    lasers.clear()

    for i, row in enumerate(tilemap):
        for j, col in enumerate(row):
            if col == ".":
                continue

            if col == "P" and not reload:
                game.respawn_point = (j * consts.TS, i * consts.TS)
                for player in game.players:
                    player.rect.topleft = game.respawn_point
                    player.stop()

            elif col == "B":
                add_block(j, i, "box", {"vel_y": 0, "dx": 0})
            elif col == "G":
                add_block(j, i, "flag")
            elif col == "S":
                add_block(j, i, "spike")
            elif col == "T":
                add_block(j, i, "trampoline")
            elif col == "m":
                add_block(j, i, "moving", {"speed": 3, "direction": 1})
            elif col == "e":
                props = {"speed": 3, "direction": 1, "cd": 0, "frame_index": 0}
                add_block(j, i, "enemy", props)
            elif col == "s":
                add_block(j, i, "shooter", {"cooldown": 12})
            elif col == "a":
                add_block(j, i, "aimbot", {"cd": 12, "d": [1, 1]})
            elif col == "-":
                lasers.append(
                    [
                        [j * consts.TS, i * consts.TS + 30],
                        [(j + 1) * consts.TS, i * consts.TS + 30],
                    ]
                )
            elif col == "g":
                add_block(j, i, "grass")
            elif col == "d":
                add_block(j, i, "dirt")
            elif col == "f":
                props = {
                    "vel_y": 0,
                    "state": "fly",
                    "pos": i * consts.TS,
                    "cd": 0,
                }
                add_block(j, i, "falling", props)
            elif col == "c":
                add_block(j, i, "checkpoint", {"status": "inactive"})

def draw_block(block):
    rect, img, name, props = block

    if not game.camera.on_screen(rect):
        return

    if name == "enemy":
        props["cd"] += 1
        if props["cd"] > 30:
            props["cd"] = 0
            props["frame_index"] += 1
            props["frame_index"] %= 2

        n = props["frame_index"] + 1
        img = asset_manager.get_image(f"blocks/enemy/{n}.png")
        img = pg.transform.scale(img, (consts.TS, consts.TS))

    elif "checkpoint" == name:
        status = props["status"]
        img = asset_manager.get_image(f"blocks/checkpoint/{status}.png")
        img = pg.transform.scale(img, (consts.TS, consts.TS))

    dest = (rect.x + game.camera.x, rect.y + game.camera.y)
    screen.blit(img, dest)


def update_block(block):
    rect, _, name, props = block
    if name in consts.MOVING_BLOCKS:
        # can the enemy walk forward (able to move)
        able_to_move = False
        rect.x += props["speed"] * props["direction"]
        for s_block in blocks:
            if not (
                s_block != block
                and s_block[2] in (consts.SOLID_BLOCKS + ["enemy", "moving"])
                and s_block[2] != "falling"
            ):
                continue

            if rect.colliderect(s_block[0]):
                props["direction"] *= -1

            if name == "enemy":
                if s_block[0].collidepoint(
                    rect.centerx + 20 * props["direction"], rect.bottom + 10
                ):
                    able_to_move = True

        if name == "enemy":
            if not able_to_move:
                props["direction"] *= -1

            for player in game.players:
                if not (player.alive and player.velrect().colliderect(rect)):
                    continue

                if player.vel_y > 1:
                    player.vel_y = -10
                    player.rotating = True
                    asset_manager.play_sound("enemy_hit.wav")

                    if block in blocks:
                        blocks.remove(block)

                else:
                    player.kill()

    elif name == "shooter":
        props["cooldown"] -= 1

        if props["cooldown"] <= 0 and (
            -game.camera.x - 100 < rect.centerx < -game.camera.x + 100 + consts.W
        ):
            bullets.append([Vec(rect.center), Vec(1, 0)])
            bullets.append([Vec(rect.center), Vec(-1, 0)])
            props["cooldown"] = 120
            asset_manager.play_sound("shoot.wav")

    elif name == "aimbot":
        props["cd"] -= 1
        if props["cd"] > 0:
            return

        alive_players = [p for p in game.players if p.alive]

        if not alive_players:
            return

        target = random.choice(alive_players).rect

        diff = Vec(target.center) - rect.center
        dist = hypot(diff.x, diff.y)

        if dist > consts.TS * 9:
            return

        for b in blocks:
            if b[0].clipline(target.center, rect.center):
                return

        vel = diff / dist

        bullets.append([Vec(rect.center), vel])
        props["cd"] = 1.0 * consts.FPS
        asset_manager.play_sound("shoot.wav")

    elif name == "falling":
        if props["state"] == "fall":
            if props["cd"] > 0:
                props["cd"] -= 1
            else:
                props["vel_y"] += consts.GRAVITY
                rect.y += props["vel_y"]
                if rect.y > props["pos"] + 25 * consts.TS:
                    props["state"] = "fly"

        elif props["state"] == "fly":
            props["cd"] = 0.2 * consts.FPS
            props["vel_y"] = 0
            rect.y = props["pos"]

    elif name == "trampoline":
        for player in game.players:
            if not player.alive or player.able_to_jump:
                continue

            p_rect = pg.Rect(
                player.rect.x,
                player.rect.y,
                player.rect.width,
                player.rect.height,
            )

            block_hitbox = pg.Rect(
                rect.x,
                rect.y + (consts.TS * 0.4),
                rect.width,
                rect.height - (consts.TS * 0.4),
            )

            if p_rect.colliderect(block_hitbox):
                player.vel_y = consts.TRAMPOLINE_VEL
                asset_manager.play_sound("trampoline.wav")
                player.rotating = True

    elif name == "checkpoint":
        if props["status"] == "active":
            return

        for player in game.players:
            if not (player.alive and player.rect.colliderect(rect)):
                continue

            asset_manager.play_sound("checkpoint.wav")
            props["status"] = "active"
            game.respawn_point = rect.topleft

    elif name == "box":
        props["vel_y"] += consts.GRAVITY
        vel_rect = pg.Rect(
            rect.x, rect.y + props["vel_y"],
            consts.TS, consts.TS
        )
        for other in blocks:
            o_rect, _, o_name, _ = other
            if not (block != other and o_rect.colliderect(vel_rect)):
                continue

            if o_name == "enemy" and props["vel_y"] > 2:
                props["vel_y"] = -6
                asset_manager.play_sound("enemy_hit.wav")
                if other in blocks:
                    blocks.remove(other)

            elif o_name in consts.SOLID_BLOCKS:
                props["vel_y"] = 0

            elif o_name == "trampoline":
                props["vel_y"] = consts.TRAMPOLINE_VEL

        for player in game.players:
            if not (player.alive and props["vel_y"] > 2):
                continue

            if player.rect.colliderect(vel_rect):
                props["vel_y"] = -6
                player.kill()

        rect.y += props["vel_y"]
        rect.x += props["dx"]
        props["dx"] = 0

    elif name == "flag":
        for player in game.players:
            if rect.colliderect(player.rect):
                break
        else:
            return

        asset_manager.play_sound("level_completed.wav")

        for player in game.players:
            player.stop()

        load_level(game.current_level + 1)

    elif name == "spike":
        rect = pg.Rect(rect.x, rect.y + (rect.height / 2), rect.width, rect.height / 2)
        for player in game.players:
            if player.alive and player.velrect().colliderect(rect):
                player.kill()


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

