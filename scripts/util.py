from .button import *
import pygame as pg
import datetime
import os
from math import atan2, sin, cos
from .consts import *
from .assets import asset_manager


def palette_swap(surf, old_c, new_c):
    img_copy = surf.copy()
    img_copy.fill(new_c)
    surf.set_colorkey(old_c)
    img_copy.blit(surf, (0, 0))
    return img_copy


def draw_text(surface, centered, size, smthing, color, x, y):
    text = asset_manager.get_font(size).render(smthing, True, color)

    if centered:
        text_rect = text.get_rect(center=(x, y))
        surface.blit((text), text_rect)

    else:
        surface.blit(text, (x, y))

    return text


def draw_image(surface, img, scalex, scaley, px, centered, x, y):
    img = pg.image.load(img)

    if px:
        image = pg.transform.scale(img, (scalex, scaley))

    else:
        image = pg.transform.scale(
            img,
            (img.get_width() * scalex, img.get_height() * scaley)
        )

    if centered:
        image_rect = image.get_rect(center=(x, y))
        surface.blit((image), image_rect)

    else:
        surface.blit(image, (x, y))

    return img


def move_towards_rect(r1, r2, speed):
    radians = atan2(r2.centery - r1.centery, r2.centerx -
                    r1.centerx)  # Y van elol!

    dx = cos(radians)*speed
    dy = sin(radians)*speed

    r1.centerx += dx
    r1.centery += dy


KSS = 30  # keystroke size
KSG = 8  # keystroke gap

KSP_C = (120, 120, 120)  # keydown color
KSU_C = (0,   0,   255)  # keyup color


def draw_keystroke(surf, key, x, y, text):
    rect = pg.Rect(x, y, KSS, KSS)
    if key:
        pg.draw.rect(surf, KSP_C, rect)
    else:
        pg.draw.rect(surf, KSU_C, rect)
    draw_text(surf, True, int(KSS/2), text, WHITE, rect.centerx,
        rect.centery + 7 if text == '^' else rect.centery)


def keystrokes(surf, tipus):
    keys = pg.key.get_pressed()
    if tipus == 'wasd':
        draw_keystroke(surf, keys[pg.K_a], KSG, H-KSG-KSS,        'a')
        draw_keystroke(surf, keys[pg.K_w], KSG*2+KSS, H-KSG-KSS,  'w')
        draw_keystroke(surf, keys[pg.K_d], KSG*3+KSS*2, H-KSG-KSS, 'd')

    elif tipus == 'arrows':
        e = W-((KSS*3)+(KSG*4))
        draw_keystroke(surf, keys[pg.K_LEFT],
                       KSG+e, H-KSG-KSS,           '<')
        draw_keystroke(surf, keys[pg.K_UP], KSG*2+KSS+e, H-KSG-KSS, '^')
        draw_keystroke(surf, keys[pg.K_RIGHT],
                       KSG*3+KSS*2+e, H-KSG-KSS,   '>')


def screenshot():
    screen = pg.display.get_surface()
    ss_s = screen.copy()
    ss_id = 1
    date = datetime.date.today()
    file = f'screenshots/{date}_{ss_id}.png'
    while os.path.exists(file):
        ss_id += 1
        file = f'screenshots/{date}_{ss_id}.png'

    pg.image.save(ss_s, file)


