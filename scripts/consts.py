# Import pygame library and alias it as 'pg' for shorter reference throughout the game
import pygame as pg

# Define the gravitational acceleration constant that pulls objects downward each frame
GRAVITY = 0.6
# Set the negative velocity boost that trampolines give to players when bounced upon
TRAMPOLINE_VEL = -20
# Define the horizontal movement speed of players in pixels per frame
PLAYER_SPEED = 7
# Set the tile size in pixels - each game tile is 60x60 pixels
TS = 60
# Define the number of columns in the game grid for level layout
COL = 44
# Define the number of rows in the game grid for level layout
ROW = 12
# Set the window width and height dimensions in pixels (1280x720 for 720p resolution)
W, H = (1280, 720)
# Calculate the center coordinates of the screen for camera positioning and UI centering
CX, CY = (W//2, H//2)
# Set the target frames per second for consistent game timing
FPS = 60
# Create a pygame clock object to control the game's frame rate and timing
clock = pg.time.Clock()

# Define pure white color as RGB tuple for UI elements and text
WHITE = (255, 255, 255)
# Define pure black color as RGB tuple for backgrounds and outlines
BLACK = (0, 0, 0)
# Define pure red color as RGB tuple for danger elements and player coloring
RED = (255, 0, 0)
# Define pure blue color as RGB tuple for water elements and player coloring
BLUE = (0, 0, 255)
# Define light blue color as RGB tuple for sky elements and UI highlights
LBLUE = (60, 120, 255)
# Define dark blue color as RGB tuple for deep water and menu backgrounds
DBLUE = (0, 0, 180)
# Define pure green color as RGB tuple for grass elements and player coloring
GREEN = (0, 255, 0)
# Define dark green color as RGB tuple for forest elements and button states
DGREEN = (0, 200, 0)

# Set the default background color as a light blue sky tone for the game world
bg_color = 100, 180, 240

# Define the filename of the custom font used for game text rendering
FONT_NAME = 'fffforwa.ttf'
