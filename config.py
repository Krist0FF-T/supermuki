import pygame as pg

auto_fullscreen = False
flip_when_jump = True
show_deaths = False
vsync = False
audio_volume = 0.1
fullscreen = False

controls = [
    (pg.K_a, pg.K_d, pg.K_w),
    (pg.K_LEFT, pg.K_RIGHT, pg.K_UP),
]

# controls = [
#     (pg.K_q, pg.K_e, pg.K_w),
#     (pg.K_a, pg.K_d, pg.K_s),
#     (pg.K_y, pg.K_c, pg.K_x),
#     # (pg.K_KP_4, pg.K_KP_6, pg.K_KP_8),
# ]
