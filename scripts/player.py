
from typing import TYPE_CHECKING
import pygame as pg

from scripts import consts, util
from scripts.assets import asset_manager
import config

if TYPE_CHECKING:
    from .game import Game

class Player:
    def __init__(self, game, num: int):
        self.game: Game = game

        # graphical -----
        self.color = [255, 0, 0]
        self.flip = False
        self.rotation = 0.0
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
        self.vel_x = 0.0
        self.vel_y = 0.0
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
            if abs(self.rotation) > 355:
                self.rotation = 0.0
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
            self.game.camera.preferred = self
            dx = movement_dir * self.speed
            self.direction = movement_dir

        if self.alive and self.jump and (self.game.flying or self.able_to_jump):
            self.vel_y = consts.JUMP_VEL
            self.rotating = True
            self.jump = False

        dy += self.vel_y
        dx += self.vel_x

        for block in self.game.blocks:
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
                        self.vel_y = 0.0
                        self.able_to_jump = True
                        dy = b_rect.top - self.rect.bottom

                    dx = b_props["speed"] * b_props["direction"]

            if b_rect.colliderect(
                (self.rect.x + dx, self.rect.y),
                (self.rect.width, self.rect.height),
            ):
                self.vel_x = 0.0
                if not (b_name == "box" and self.able_to_jump):
                    dx = 0
                    continue

                dx = int(dx * 0.3)
                x_collide = False
                for col_block in self.game.blocks:
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
                    self.vel_y = 0.0
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
                    self.rotation = 0.0

        if abs(self.vel_y) >= 5:
            self.able_to_jump = False

        self.rect.x += dx
        self.rect.y += dy

    def stop(self):
        self.vel_y = 0.0
        self.vel_x = 0.0
        self.jump = False
        self.left = False
        self.right = False

    def kill(self):
        if not self.alive:
            return

        asset_manager.play_sound("enemy_hit.wav")
        self.alive = False
        self.vel_y = -12.0
        self.deaths += 1

    def respawn(self):
        self.alive = True
        self.rotating = False
        self.rotation = 0.0
        self.vel_y = 0.0
        self.rect.topleft = self.game.respawn_point

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
            self.game.screen.blit(
                pg.transform.flip(fallpos_image, self.flip, False),
                (self.rect.x + self.game.camera.x, 30),
            )
            return

        if config.flip_when_jump:
            img_to_blit = pg.transform.rotate(c_img, self.rotation)
        else:
            img_to_blit = c_img

        flipped = pg.transform.flip(img_to_blit, self.flip, False)

        rect = flipped.get_rect()
        rect.centerx = self.rect.centerx + self.game.camera.x
        rect.centery = self.rect.centery + self.game.camera.y
        self.game.screen.blit(flipped, rect)

