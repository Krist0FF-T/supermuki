import pygame as pg
from . import consts, util, menu
import config

from .camera import Camera
from .player import Player
from .assets import asset_manager

import random
import os
from math import hypot

from pygame import Vector2 as Vec

class Game:
    def __init__(self):
        self.screen = pg.display.set_mode(
            (consts.W, consts.H),
            vsync=config.vsync,
        )
        pg.display.set_caption("SuperMuki")

        self.current_level = 1

        self.players: list[Player] = []
        self.camera = Camera(self)
        self.respawn_point = (0.0, 0.0)

        self.flying = False

        self.blocks = []
        self.bullets = []
        self.lasers = []

        self.bg_lines = []
        for i in range(22):
            x = i * 4 * consts.W / 25
            self.bg_lines.append([
                [x - consts.H, 0],
                [x, consts.H]
            ])

    def run(self):
        asset_manager.load_player_imgs()
        asset_manager.set_audio_volume(config.audio_volume)

        self.main_menu()
        self.color_selection()
        level = menu.level_selection(self.screen)
        self.load_level(1 if level is None else level)

        while True:
            if not config.vsync:
                consts.clock.tick(consts.FPS)

            for event in pg.event.get():
                self.handle_event(event)

            self.update()
            self.draw()

    def main_menu(self):
        # n = menu.main_menu(self.screen)
        n = len(config.controls)
        self.players = [Player(self, i + 1) for i in range(n)]

    def pause(self):
        for player in self.players:
            player.stop()

        ret = menu.pause_menu(self.screen)
        if ret == menu.code.LEVEL_SELECT:
            level = menu.level_selection(self.screen)
            self.load_level(level)

        elif ret == menu.code.MAIN_MENU:
            self.main_menu()

            for player in self.players:
                player.deaths = 0

            self.color_selection()
            level = menu.level_selection(self.screen)
            self.load_level(level)

        elif ret == menu.code.COLOR_SELECT:
            self.color_selection()

    def color_selection(self):
        colors = [p.color for p in self.players]
        menu.color_selection(self.screen, colors)
        for player in self.players:
            print(player.color)
            player.images = util.recolor_player(player.color)


    def _draw_stats(self):
        util.draw_text(self.screen, False, 30, f"level {self.current_level}", "white", 15, 15)

        if self.flying:
            util.draw_text(self.screen, True, 20, "fly", "white", consts.CX, 30)

        if config.show_deaths:
            util.draw_text(self.screen, True, 30, "deaths", "white", consts.W - 80, 30)
            for player in self.players:
                util.draw_text(
                    self.screen,
                    True,
                    30,
                    f"{player.deaths}",
                    player.color,
                    consts.W - 200 + (80 * player.num),
                    90,
                )

    def draw(self):
        self.screen.fill(consts.GAME_BG_COLOR)

        self.draw_bg_lines()

        for block in self.blocks:
            self.draw_block(block)

        for player in self.players:
            player.draw()

        for bullet in self.bullets:
            if not - consts.BULLET_R < bullet[0].x + self.camera.x < consts.BULLET_R + consts.W:
                continue

            pos = (bullet[0].x + self.camera.x, bullet[0].y)
            pg.draw.circle(self.screen, "blue", pos, consts.BULLET_R)

        for laser in self.lasers:
            pg.draw.line(
                self.screen,
                "red",
                (laser[0][0] + self.camera.x, laser[0][1] + self.camera.y),
                (laser[1][0] + self.camera.x, laser[1][1] + self.camera.y),
                5,
            )

        self._draw_stats()

        pg.display.update()

    def update(self):
        for player in self.players:
            player.move()
            player.update()

            if not player.alive:
                continue

            for laser in self.lasers:
                if player.rect.clipline(laser):
                    player.kill()

        for block in self.blocks:
            self.update_block(block)

        for bullet in self.bullets:
            self.update_bullet(bullet)

        self.camera.update()

    def handle_event(self, event: pg.Event):
        if event.type == pg.QUIT:
            util.close()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_k:
                self.flying = not self.flying

            elif event.key == pg.K_r:
                self.load_level(reload = not event.mod & pg.KMOD_LSHIFT)

            elif event.key == pg.K_F2:
                util.screenshot()
                self.pause()

            elif event.key in (pg.K_ESCAPE, pg.K_SPACE):
                self.pause()

            elif event.key == pg.K_F11:
                config.fullscreen = not config.fullscreen
                pg.display.toggle_fullscreen()

        if event.type in (pg.KEYDOWN, pg.KEYUP):
            down = event.type == pg.KEYDOWN

            for player, controls in zip(self.players, config.controls):
                if event.key == controls[0]:
                    player.left = down
                elif event.key == controls[1]:
                    player.right = down
                elif event.key == controls[2]:
                    player.jump = down


    def load_level(self, num: int | None = None, reload=False):
        if num is not None:
            self.current_level = num

        file_name = f"assets/levels/{self.current_level}.txt"

        if not os.path.exists(file_name):
            level = menu.level_selection(self.screen)
            self.load_level(level)
            return

        with open(file_name, "r") as f:
            tilemap = f.readlines()

        for player in self.players:
            if reload:
                player.rect.topleft = self.respawn_point
            else:
                player.deaths = 0

        self.blocks.clear()
        self.bullets.clear()
        self.lasers.clear()

        for i, row in enumerate(tilemap):
            for j, col in enumerate(row):
                if col == ".":
                    continue

                if col == "P" and not reload:
                    self.respawn_point = (j * consts.TS, i * consts.TS)
                    for player in self.players:
                        player.rect.topleft = self.respawn_point
                        player.stop()

                elif col == "B":
                    self.add_block(j, i, "box", {"vel_y": 0, "dx": 0})
                elif col == "G":
                    self.add_block(j, i, "flag")
                elif col == "S":
                    self.add_block(j, i, "spike")
                elif col == "T":
                    self.add_block(j, i, "trampoline")
                elif col == "m":
                    self.add_block(j, i, "moving", {"speed": 3, "direction": 1})
                elif col == "e":
                    props = {"speed": 3, "direction": 1, "cd": 0, "frame_index": 0}
                    self.add_block(j, i, "enemy", props)
                elif col == "s":
                    self.add_block(j, i, "shooter", {"cooldown": 12})
                elif col == "a":
                    self.add_block(j, i, "aimbot", {"cd": 12, "d": [1, 1]})
                elif col == "-":
                    self.lasers.append(
                        [
                            [j * consts.TS, i * consts.TS + 30],
                            [(j + 1) * consts.TS, i * consts.TS + 30],
                        ]
                    )
                elif col == "g":
                    self.add_block(j, i, "grass")
                elif col == "d":
                    self.add_block(j, i, "dirt")
                elif col == "f":
                    props = {
                        "vel_y": 0,
                        "state": "fly",
                        "pos": i * consts.TS,
                        "cd": 0,
                    }
                    self.add_block(j, i, "falling", props)
                elif col == "c":
                    self.add_block(j, i, "checkpoint", {"status": "inactive"})

    def add_block(self, x, y, name, properties={}):
        img = asset_manager.get_image(f"blocks/{name}.png").convert_alpha()

        w = 2 if name == "moving" else 1
        image = pg.transform.scale(img, (consts.TS * w, consts.TS))

        rect = image.get_rect()
        rect.topleft = x * consts.TS, y * consts.TS
        block = [rect, image, name, properties]
        self.blocks.append(block)


    def update_block(self, block):
        rect, _, name, props = block
        if name in consts.MOVING_BLOCKS:
            # can the enemy walk forward (able to move)
            able_to_move = False
            rect.x += props["speed"] * props["direction"]
            for s_block in self.blocks:
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

            for player in self.players:
                if not (player.alive and player.velrect().colliderect(rect)):
                    continue

                if player.vel_y > 1:
                    player.vel_y = -10.0
                    player.rotating = True
                    asset_manager.play_sound("enemy_hit.wav")

                    if block in self.blocks:
                        self.blocks.remove(block)

                else:
                    player.kill()

        elif name == "shooter":
            props["cooldown"] -= 1

            if props["cooldown"] <= 0 and (
                -self.camera.x - 100 < rect.centerx < -self.camera.x + 100 + consts.W
            ):
                self.bullets.append([Vec(rect.center), Vec(1, 0)])
                self.bullets.append([Vec(rect.center), Vec(-1, 0)])
                props["cooldown"] = 120
                asset_manager.play_sound("shoot.wav")

        elif name == "aimbot":
            props["cd"] -= 1
            if props["cd"] > 0:
                return

            alive_players = [p for p in self.players if p.alive]

            if not alive_players:
                return

            target = random.choice(alive_players).rect

            diff = Vec(target.center) - rect.center
            dist = hypot(diff.x, diff.y)

            if dist > consts.TS * 9:
                return

            for b in self.blocks:
                if (
                    b[2] in consts.SOLID_BLOCKS
                    and b[0].clipline(target.center, rect.center)
                ):
                    return

            vel = diff / dist

            self.bullets.append([Vec(rect.center), vel])
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
            for player in self.players:
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

            for player in self.players:
                if not (player.alive and player.rect.colliderect(rect)):
                    continue

                asset_manager.play_sound("checkpoint.wav")
                props["status"] = "active"
                self.respawn_point = rect.topleft

        elif name == "box":
            props["vel_y"] += consts.GRAVITY
            vel_rect = pg.Rect(
                rect.x, rect.y + props["vel_y"],
                consts.TS, consts.TS
            )
            for other in self.blocks:
                o_rect, _, o_name, _ = other
                if not (block != other and o_rect.colliderect(vel_rect)):
                    continue

                if o_name == "enemy" and props["vel_y"] > 2:
                    props["vel_y"] = -6
                    asset_manager.play_sound("enemy_hit.wav")
                    if other in self.blocks:
                        self.blocks.remove(other)

                elif o_name in consts.SOLID_BLOCKS:
                    props["vel_y"] = 0

                elif o_name == "trampoline":
                    props["vel_y"] = consts.TRAMPOLINE_VEL

            for player in self.players:
                if not (player.alive and props["vel_y"] > 2):
                    continue

                if player.rect.colliderect(vel_rect):
                    props["vel_y"] = -6
                    player.kill()

            rect.y += props["vel_y"]
            rect.x += props["dx"]
            props["dx"] = 0

        elif name == "flag":
            for player in self.players:
                if rect.colliderect(player.rect):
                    break
            else:
                return

            asset_manager.play_sound("level_completed.wav")

            for player in self.players:
                player.stop()

            self.load_level(self.current_level + 1)

        elif name == "spike":
            rect = pg.Rect(rect.x, rect.y + (rect.height / 2), rect.width, rect.height / 2)
            for player in self.players:
                if player.alive and player.velrect().colliderect(rect):
                    player.kill()


    def draw_block(self, block):
        rect, img, name, props = block

        if not self.camera.on_screen(rect):
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

        dest = (rect.x + self.camera.x, rect.y + self.camera.y)
        self.screen.blit(img, dest)

    def draw_bg_lines(self):
        color = (
            consts.GAME_BG_COLOR[0] + 4,
            consts.GAME_BG_COLOR[1] + 4,
            consts.GAME_BG_COLOR[2] + 7,
        )
        camx = self.camera.x * 0.5
        camy = self.camera.y * 0.5
        for line in self.bg_lines:
            if -camx - consts.W - consts.H < line[0][0] - consts.W < -camx:
                pg.draw.line(
                    self.screen,
                    color,
                    (line[0][0] + camx, line[0][1] + camy),
                    (line[1][0] + camx, line[1][1] + camy),
                    40,
                )

    def update_bullet(self, bullet: list[Vec]):
        bullet[0] += 7 * bullet[1]
        bullet_rect = pg.Rect(bullet[0].x - 10, bullet[0].y - 10, 20, 20)

        for player in self.players:
            if player.rect.colliderect(bullet_rect):
                player.kill()

        if consts.COL * consts.TS < bullet[0].x < 0:
            self.bullets.remove(bullet)
            return

        for block in self.blocks:
            if (
                block[2] in consts.SOLID_BLOCKS
                and block[0].colliderect(bullet_rect)
            ):
                self.bullets.remove(bullet)
                return
