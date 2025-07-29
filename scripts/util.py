# Import all button-related functions and classes from the button module
from .button import *
# Import pygame library for graphics, image manipulation, and keyboard input
import pygame as pg
# Import datetime module for generating timestamps in screenshot filenames
import datetime
# Import os module for file system operations like checking file existence
import os
# Import math functions for calculating angles and trigonometric operations
from math import atan2, sin, cos
# Import all constants including colors, dimensions, and game settings
from .consts import *
# Import asset manager to access fonts and other game assets
from .assets import asset_manager


# Function to swap one color with another in a surface, used for player customization
def palette_swap(surf, old_c, new_c):
    # Create a copy of the original surface to avoid modifying the original
    img_copy = surf.copy()
    # Fill the copied surface with the new color to replace old color with
    img_copy.fill(new_c)
    # Set the old color as transparent in the original surface
    surf.set_colorkey(old_c)
    # Blit the original surface onto the new colored surface, replacing old color
    img_copy.blit(surf, (0, 0))
    # Return the surface with the color successfully swapped
    return img_copy


# Function to render and draw text onto a surface with various positioning options
def draw_text(surface, centered, size, smthing, color, x, y):
    # Render the text string using the asset manager's font at specified size and color
    text = asset_manager.get_font(size).render(smthing, True, color)

    # Check if the text should be centered at the given coordinates
    if centered:
        # Get a rectangle for the text positioned with center at (x, y)
        text_rect = text.get_rect(center=(x, y))
        # Blit the text surface onto the target surface at the centered position
        surface.blit((text), text_rect)

    # If not centered, position text with top-left corner at (x, y)
    else:
        # Blit the text surface directly at the specified coordinates
        surface.blit(text, (x, y))

    # Return the rendered text surface for potential reuse
    return text


# Function to load, scale, and draw an image onto a surface with flexible scaling options
def draw_image(surface, img, scalex, scaley, px, centered, x, y):
    # Load the image from the file path provided
    img = pg.image.load(img)

    # Check if px parameter is True, indicating pixel-exact scaling
    if px:
        # Scale the image to exact pixel dimensions specified
        image = pg.transform.scale(img, (scalex, scaley))

    # Otherwise use scale factors to multiply original dimensions
    else:
        # Scale image by multiplying original width and height by scale factors
        image = pg.transform.scale(
            img,
            (img.get_width() * scalex, img.get_height() * scaley)
        )

    # Check if the image should be centered at the given coordinates
    if centered:
        # Get a rectangle for the image positioned with center at (x, y)
        image_rect = image.get_rect(center=(x, y))
        # Blit the scaled image onto the surface at the centered position
        surface.blit((image), image_rect)

    # If not centered, position image with top-left corner at (x, y)
    else:
        # Blit the scaled image directly at the specified coordinates
        surface.blit(image, (x, y))

    # Return the original image for potential further use
    return img


# Function to move rectangle r1 towards rectangle r2 at a specified speed
def move_towards_rect(r1, r2, speed):
    # Calculate the angle in radians from r1's center to r2's center
    radians = atan2(r2.centery - r1.centery, r2.centerx -
                    r1.centerx)  # Y van elol!

    # Calculate horizontal movement component using cosine of the angle
    dx = cos(radians)*speed
    # Calculate vertical movement component using sine of the angle  
    dy = sin(radians)*speed

    # Move r1's center horizontally by the calculated dx amount
    r1.centerx += dx
    # Move r1's center vertically by the calculated dy amount
    r1.centery += dy


# Define the size of each keystroke indicator box in pixels
KSS = 30  # keystroke size
# Define the gap between keystroke indicator boxes in pixels
KSG = 8  # keystroke gap

# Define the color for keystroke indicators when key is pressed (gray)
KSP_C = (120, 120, 120)  # keydown color
# Define the color for keystroke indicators when key is not pressed (blue)
KSU_C = (0,   0,   255)  # keyup color


# Function to draw a single keystroke indicator with appropriate color and text
def draw_keystroke(surf, key, x, y, text):
    # Create a rectangle for the keystroke indicator at specified position
    rect = pg.Rect(x, y, KSS, KSS)
    # Check if the key is currently being pressed
    if key:
        # Draw the rectangle in pressed color (gray) when key is down
        pg.draw.rect(surf, KSP_C, rect)
    # If key is not pressed, use the unpressed color
    else:
        # Draw the rectangle in unpressed color (blue) when key is up
        pg.draw.rect(surf, KSU_C, rect)
    # Draw the key label text centered in the rectangle, adjusting position for '^' character
    draw_text(surf, True, int(KSS/2), text, WHITE, rect.centerx,
              rect.centery + 7 if text == '^' else rect.centery)


# Function to display keystroke indicators for either WASD or arrow key sets
def keystrokes(surf, tipus):
    # Get the current state of all keyboard keys for checking which are pressed
    keys = pg.key.get_pressed()
    # Check if we should display WASD key indicators
    if tipus == 'wasd':
        # Draw 'A' key indicator on the left side of the screen
        draw_keystroke(surf, keys[pg.K_a], KSG, H-KSG-KSS,        'a')
        # Draw 'W' key indicator to the right of 'A' key
        draw_keystroke(surf, keys[pg.K_w], KSG*2+KSS, H-KSG-KSS,  'w')
        # Draw 'D' key indicator to the right of 'W' key
        draw_keystroke(surf, keys[pg.K_d], KSG*3+KSS*2, H-KSG-KSS, 'd')

    # Check if we should display arrow key indicators
    elif tipus == 'arrows':
        # Calculate the starting x position for arrow keys on the right side of screen
        e = W-((KSS*3)+(KSG*4))
        # Draw left arrow key indicator
        draw_keystroke(surf, keys[pg.K_LEFT],
                       KSG+e, H-KSG-KSS,           '<')
        # Draw up arrow key indicator to the right of left arrow
        draw_keystroke(surf, keys[pg.K_UP], KSG*2+KSS+e, H-KSG-KSS, '^')
        # Draw right arrow key indicator to the right of up arrow
        draw_keystroke(surf, keys[pg.K_RIGHT],
                       KSG*3+KSS*2+e, H-KSG-KSS,   '>')


# Function to capture and save a screenshot of the current game screen
def screenshot():
    # Get the current display surface (main game screen)
    screen = pg.display.get_surface()
    # Create a copy of the screen surface to save as screenshot
    ss_s = screen.copy()
    # Initialize screenshot ID counter for unique filenames
    ss_id = 1
    # Get today's date for the screenshot filename
    date = datetime.date.today()
    # Create the initial filename using date and ID
    file = f'screenshots/{date}_{ss_id}.png'
    # Check if a file with this name already exists
    while os.path.exists(file):
        # Increment the ID to avoid overwriting existing screenshots
        ss_id += 1
        # Generate a new filename with the incremented ID
        file = f'screenshots/{date}_{ss_id}.png'

    # Save the screenshot surface to the unique filename as PNG
    pg.image.save(ss_s, file)
