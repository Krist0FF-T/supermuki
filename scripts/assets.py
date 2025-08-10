import pygame as pg
from . import consts


class AssetManager:
    def __init__(self):
        pg.mixer.init()
        pg.display.init()
        pg.font.init()

        self.images: dict[str, pg.Surface] = {}
        self.sounds: dict[str, pg.Sound] = {}
        self.font_cache: dict[int, pg.Font] = {}
        self.player_images: list[pg.Surface] = []

        self.audio_volume = 1.0

    def play_sound(self, name: str):
        sound = self.get_sound(name)
        sound.set_volume(self.audio_volume)
        sound.play()

    def get_sound(self, name: str) -> pg.Sound:
        sound = self.sounds.get(name)

        if sound is None:
            path = f"assets/sound/{name}"
            print("loading sound", name)
            sound = pg.mixer.Sound(path)
            self.sounds[name] = sound

        return sound

    def get_image(self, name: str) -> pg.Surface:
        img = self.images.get(name)
        if img is None:
            path = f"assets/img/{name}"
            img = pg.image.load(path)
            print("loading image", name)
            self.images[name] = img
        return img

    def get_font(self, size: int = 20) -> pg.Font:
        font = self.font_cache.get(size)
        if font is None:
            print("creating font", size)
            font = pg.Font(consts.FONT, size)
            self.font_cache[size] = font
        return font

    def load_player_imgs(self):
        self.player_images.clear()
        for i in range(1, 4):
            img = self.get_image(f"player/{i}.png").convert()
            img.set_colorkey((0, 0, 0))
            img = pg.transform.scale(img, (27, 27))
            self.player_images.append(img)

    def set_audio_volume(self, f: float):
        self.audio_volume = f


asset_manager = AssetManager()
