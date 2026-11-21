import pygame as pg

clock = pg.time.Clock()
FPS = 60
W, H = (1280, 720)
CX, CY = (W // 2, H // 2)

GRAVITY = 0.6
PLAYER_SPEED = 7.0
JUMP_VEL = -10.0
TRAMPOLINE_VEL = -20.0

COL = 44
ROW = 12
BULLET_SPEED = 7.0
BULLET_R = 10
TS = 60

SOLID_BLOCKS = ["grass", "dirt", "falling", "moving", "box", "enemy"]
MOVING_BLOCKS = ["moving", "enemy"]

GAME_BG_COLOR = (100, 180, 240)
GUI_BG_COLOR = (50, 50, 50)

FONT = "assets/fonts/fffforwa.ttf"

