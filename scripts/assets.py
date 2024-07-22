import pygame as pg
from .consts import *
# from pygame.image import load
# from pygame.transform import scale

pg.mixer.init()
pg.display.init()
pg.font.init()

class AssetManager:
    def __init__(self):
        self.loaded = {}


    def get_sound(self, name):
        path = f"assets/sound/{name}"

        if path in self.loaded:
            return self.loaded[path]

        return pg.mixer.Sound(path)


    def get_image(self, name):
        path = f"assets/img/{name}"

        if path in self.loaded:
            return self.loaded[path]

        return pg.image.load(path)


    def get_font(self, size: int=20, name=FONT_NAME):
        return pg.Font(f"assets/fonts/{name}", size)


    def load_player_imgs(self, path="player"):
        self.player_images = []
        for i in range(1, 4):
            img = self.get_image(f"{path}/{i}.png").convert()
            img.set_colorkey((0, 0, 0))
            img = pg.transform.scale(img, (27, 27))
            self.player_images.append(img)



asset_manager = AssetManager()

# # sounds
# load_sound = lambda name: pg.mixer.Sound(f"assets/sound/{name}")
# trampoline_fx = load_sound("trampoline.wav")
# trampoline_fx.set_volume(0.2)
# completed_fx = load_sound("level_completed.wav")
# completed_fx.set_volume(0.4)
#
# enemy_hit_fx = load_sound("enemy_hit.wav")
#
# checkpoint_fx = load_sound("checkpoint.wav")
# shoot_fx = load_sound("shoot.wav")
# laser_fx = load_sound("laser.wav")
#
# # images
#
# player_images = []
# for i in range(1, 4):
#     img = pg.image.load(f'assets/img/player/{i}.png').convert()
#     img.set_colorkey((0, 0, 0))
#     img = pg.transform.scale(img, (27, 27))
#     player_images.append(img)
#
# enemy_images = [
#     scale(load(f'assets/img/blocks/enemy/{i}.png'), (TS, TS))
#     for i in [1, 2]
# ]
#
# _checkpoint_f = 'assets/img/blocks/checkpoint'
# checkpoint_images = dict(
#     active = scale(load(f'{_checkpoint_f}/active.png'),   (TS, TS)),
#     inactive = scale(load(f'{_checkpoint_f}/inactive.png'), (TS, TS)),
# )
#
# def gen_b_imgs(names: list[str]):
#     return {
#         name: load(f'assets/img/blocks/{name}.png')
#         for name in names
#     }
#
# b_imgs = gen_b_imgs([
#     'enemy', 'grass', 'dirt', 'trampoline', 'moving', 'box', 'flag', 'shooter',
#     'falling', 'spike', 'checkpoint', 'aimbot'
# ])



