import datetime
import os
import sys
import pygame as pg

from .assets import asset_manager


def recolor_player(color) -> list[pg.Surface]:
    imgs = []
    for c_img in asset_manager.player_images:
        p_img = c_img.copy()
        p_img.fill(color)
        c_img.set_colorkey(c_img.get_at((0, 0)))
        p_img.blit(c_img, (0, 0))
        p_img.set_colorkey((0, 0, 0))
        imgs.append(p_img)
    return imgs


def draw_text(
    surf: pg.Surface,
    centered: bool,
    size: int,
    text: str,
    color,
    x: int,
    y: int,
) -> pg.Surface:
    text_surf = asset_manager.get_font(size).render(text, True, color)

    surf.blit(
        text_surf,
        (x, y) if not centered else text_surf.get_rect(center=(x, y)),
    )

    return text_surf


def screenshot():
    screen = pg.display.get_surface()

    if screen is None:
        return

    ss_s = screen.copy()
    ss_id = 1
    date = datetime.date.today()
    file = f'screenshots/{date}_{ss_id}.png'

    while os.path.exists(file):
        ss_id += 1
        file = f'screenshots/{date}_{ss_id}.png'

    pg.image.save(ss_s, file)


def close():
    pg.quit()
    sys.exit()

