# Import pygame library for asset loading and management functionality
import pygame as pg
# Import all constants including font names and other configuration values
from .consts import *
# from pygame.image import load
# from pygame.transform import scale

# Initialize the pygame mixer module for sound loading and playback
pg.mixer.init()
# Initialize the pygame display module for screen and image functionality
pg.display.init()
# Initialize the pygame font module for text rendering capabilities
pg.font.init()

# Define the AssetManager class to handle loading and caching of game assets
class AssetManager:
    # Initialize the asset manager with an empty cache dictionary
    def __init__(self):
        # Dictionary to store loaded assets to avoid reloading the same files
        self.loaded = {}


    # Method to load and return sound effects, with caching support
    def get_sound(self, name):
        # Construct the full file path for the sound asset
        path = f"assets/sound/{name}"

        # Check if this sound has already been loaded and cached
        if path in self.loaded:
            # Return the cached sound object to avoid reloading
            return self.loaded[path]

        # Load the sound file and return it (note: not cached in current implementation)
        return pg.mixer.Sound(path)


    # Method to load and return image files, with caching support  
    def get_image(self, name):
        # Construct the full file path for the image asset
        path = f"assets/img/{name}"

        # Check if this image has already been loaded and cached
        if path in self.loaded:
            # Return the cached image surface to avoid reloading
            return self.loaded[path]

        # Load the image file and return it (note: not cached in current implementation)
        return pg.image.load(path)


    # Method to load and return fonts with specified size and optional custom font name
    def get_font(self, size: int=20, name=FONT_NAME):
        # Load and return a font object from the assets folder with given size
        return pg.font.Font(f"assets/fonts/{name}", size)


    # Method to preload and prepare all player character sprites for the game
    def load_player_imgs(self, path="player"):
        # Initialize empty list to store processed player sprite images
        self.player_images = []
        # Loop through player sprite frames numbered 1 through 3
        for i in range(1, 4):
            # Load the player sprite image and convert it for better performance
            img = self.get_image(f"{path}/{i}.png").convert()
            # Set black color as transparent for proper sprite rendering
            img.set_colorkey((0, 0, 0))
            # Scale the sprite to 27x27 pixels for consistent game character size
            img = pg.transform.scale(img, (27, 27))
            # Add the processed sprite image to the player images list
            self.player_images.append(img)



# Create a global instance of the AssetManager for use throughout the game
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




