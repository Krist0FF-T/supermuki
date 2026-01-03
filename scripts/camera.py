import pygame as pg
from . import consts

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .player import Player
    from .game import Game

class Camera:
    def __init__(self, game):
        self.game: Game = game
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
        p1 = self.game.players[0]
        p2 = self.game.players[1] if len(self.game.players) >= 2 else None
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

