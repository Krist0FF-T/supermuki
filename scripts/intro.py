import pygame as pg
from .util import draw_text, long_fade
from .consts import W, H, WHITE
from .assets import asset_manager

def intro(surface):
    _img = asset_manager.get_image("intro.png")
    img = pg.transform.scale(_img, (W, H))

    surface.blit(img, (0,0))
    draw_text(surface, False, 60, 'Loading files...', WHITE, 20, 20)
    pg.display.update()
    pg.time.wait(1000)
    long_fade(surface)



