import pygame as pg
from supermuki import consts

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .player import Player
    from .game import Game

class Camera:
    def __init__(self, game):
        self.game: Game = game
        self.x = 0.0
        self.y = 0.0 # currently constant
        self.target_x = 0.0
        self.preferred: Player | None = None

    def on_screen(self, rect: pg.Rect) -> bool:
        return 0 < rect.right + self.x and rect.left + self.x < consts.W

    def update(self):
        p1 = self.game.players[0]
        p2 = self.game.players[1] if len(self.game.players) >= 2 else None

        if p2 is None:
            self.target_x = -p1.rect.centerx + consts.CX
        else:
            self.target_x = (
                -(p1.rect.centerx + p2.rect.centerx) / 2 + consts.CX
            )

            distance = abs(p1.rect.centerx - p2.rect.centerx)
            far_apart = distance > consts.W - 300

            if far_apart and self.preferred:
                self.target_x = -self.preferred.rect.centerx + consts.CX

        self.x += (self.target_x - self.x) * 0.05

        if self.x > 0:
            self.x = 0

        max_x = consts.TS * consts.COL_COUNT - consts.W
        if self.x < -max_x:
            self.x = -max_x

