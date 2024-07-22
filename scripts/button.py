import pygame as pg
from scripts.settings import *
from .consts import *
from .assets import asset_manager

def green_button(b_surf, b_rect, pos):
    b_surf.fill((0,255,0))
    if b_rect.collidepoint(pos):
        b_surf.fill((0,180,0))
        if pg.mouse.get_pressed()[0]:
            b_surf.fill((50,50,50))

def colored_b(b_surf, b_rect, color, pos):
    b_surf.fill(color)
    if b_rect.collidepoint(pos):
        b_surf.fill((120, 120, 120))

# Button class
class Button(pg.sprite.Sprite):
    def __init__(self, x, y, image, scale):
        img = asset_manager.get_image("button/" + image)
        self.image = pg.transform.scale(
            img,
            (
                img.get_width() * scale,
                img.get_height() * scale
            )
        )
        self.rect: pg.Rect = self.image.get_rect(center = (x, y))

    def draw(self, surface):
        surface.blit((self.image), self.rect)

## BUTTONS ##

# color selection

p1_red = Button(W, 300, 'c_s/red.png', 7)
p1_green = Button(0, 410, 'c_s/green.png', 7)
p1_blue = Button(0, 520, 'c_s/blue.png', 7)

p2_red = Button(0, 300, 'c_s/red.png', 7)
p2_green = Button(0, 410, 'c_s/green.png', 7)
p2_blue = Button(W, 520, 'c_s/blue.png', 7)

confirm_c = Button(W // 2, H // 2, 'c_s/confirm_c.png', 5)

# pause buttons
settings_b = Button(50, 50, 'settings.png', 3)
load_lvl_b = Button(50, 150, 'lvl.png', 3)
color_s_b = Button(50, 250, 'color_s.png', 3)

quit_button = Button(CX+250, CY + 50, 'simplebutton.png', 6)
resume_button = Button(CX-250, CY + 50, 'simplebutton.png', 6)

mainm_b = Button(50, H-50, 'main_menu.png', 6)
