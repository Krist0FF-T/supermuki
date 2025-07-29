# Import pygame library for sprite functionality and graphics
import pygame as pg
# Import the asset manager to load button images from the assets system
from .assets import asset_manager
# Import constants module for screen dimensions and positioning values
from . import consts


# Function to render a green button with hover and click state visual feedback
def green_button(b_surf, b_rect, pos):
    # Fill the button surface with bright green as the default state
    b_surf.fill((0, 255, 0))
    # Check if the mouse cursor is hovering over the button rectangle
    if b_rect.collidepoint(pos):
        # Change to darker green when mouse hovers over the button
        b_surf.fill((0, 180, 0))
        # Check if the left mouse button is currently being pressed
        if pg.mouse.get_pressed()[0]:
            # Fill with dark gray color to show the button is being clicked
            b_surf.fill((50, 50, 50))


# Function to render a customizable colored button with hover state
def colored_b(b_surf, b_rect, color, pos):
    # Fill the button surface with the provided custom color
    b_surf.fill(color)
    # Check if the mouse cursor is positioned over the button area
    if b_rect.collidepoint(pos):
        # Change to light gray when mouse hovers to indicate interactivity
        b_surf.fill((120, 120, 120))

# Button class definition for creating interactive button objects


# Define the Button class inheriting from pygame's Sprite class for easy management
class Button(pg.sprite.Sprite):
    # Initialize a new button with position, image file, and scaling factor
    def __init__(self, x, y, image, scale):
        # Load the button image from the assets folder using the asset manager
        img = asset_manager.get_image("button/" + image)
        # Scale the loaded image by the specified factor to fit UI design
        self.image = pg.transform.scale(
            img,
            (
                # Calculate new width by multiplying original width by scale factor
                img.get_width() * scale,
                # Calculate new height by multiplying original height by scale factor
                img.get_height() * scale
            )
        )
        # Create a rectangle for the button positioned at the center coordinates
        self.rect: pg.Rect = self.image.get_rect(center=(x, y))

    # Method to draw the button onto the provided surface
    def draw(self, surface):
        # Blit (copy) the button image onto the surface at the button's rectangle position
        surface.blit((self.image), self.rect)

## BUTTONS ## - Section for creating all button instances used throughout the game

# color selection - Buttons used in the color customization menu for players


# Create red color selection button for player 1, positioned on the right side
p1_red = Button(consts.W, 300, 'c_s/red.png', 7)
# Create green color selection button for player 1, positioned on the left side
p1_green = Button(0, 410, 'c_s/green.png', 7)
# Create blue color selection button for player 1, positioned on the left side  
p1_blue = Button(0, 520, 'c_s/blue.png', 7)

# Create red color selection button for player 2, positioned on the left side
p2_red = Button(0, 300, 'c_s/red.png', 7)
# Create green color selection button for player 2, positioned on the left side
p2_green = Button(0, 410, 'c_s/green.png', 7)
# Create blue color selection button for player 2, positioned on the right side
p2_blue = Button(consts.W, 520, 'c_s/blue.png', 7)

# Create confirmation button for color selection, centered on screen
confirm_c = Button(consts.W // 2, consts.H // 2, 'c_s/confirm_c.png', 5)

# pause buttons - Buttons displayed in the pause menu for game control
# Create button to load a different level, positioned in top-left corner
load_lvl_b = Button(50, 50, 'lvl.png', 3)
# Create button to open color selection menu, positioned below load level button
color_s_b = Button(50, 150, 'color_s.png', 3)

# Create quit button positioned to the right of screen center in pause menu
quit_button = Button(consts.CX + 250, consts.CY + 50, 'simplebutton.png', 6)
# Create resume button positioned to the left of screen center in pause menu
resume_button = Button(consts.CX - 250, consts.CY + 50, 'simplebutton.png', 6)

# Create main menu button positioned in bottom-left corner of pause menu
mainm_b = Button(50, consts.H - 50, 'main_menu.png', 6)
