# Import pygame library for graphics and game development functionality
import pygame

# Initialize pygame's font module to enable text rendering capabilities
pygame.font.init()

# Define screen width and height dimensions in pixels for the map editor
W, H = 1280, 720
# Calculate center coordinates of the screen for positioning elements
CX, CY = W/2, H/2

# Create a pygame clock object to control frame rate and timing
clock = pygame.time.Clock()
# Set target frames per second for smooth editor performance
FPS = 61

# Define tile size in pixels - each map tile is 60x60 pixels
TS = 60

# Define the number of rows in the map grid for level editing
ROWS = 12
# Define the number of columns in the map grid for level editing  
COLS = 100

# Function to render and draw text on screen with flexible positioning options
def mts(surface, rect, size, smthing, color, x, y):
    # Create a font object from the custom font file with specified size
    font = pygame.font.Font('../assets/fonts/fffforwa.ttf', size)
    # Render the text string with antialiasing and specified color
    text = font.render(smthing, 1, color)
    # Check if text should be positioned using rect centering
    if rect:
        # Get rectangle for text and center it at specified coordinates
        text_rect = text.get_rect(center = (x, y))
        # Draw text surface at the centered rectangle position
        surface.blit((text), text_rect)
    # If not using rect centering, position at exact coordinates
    elif not rect:
        # Draw text surface directly at specified x,y coordinates
        surface.blit(text, (x, y))
    # Return the rendered text surface for potential reuse
    return text

# List of all available block types for the map editor
b_names = ['aimbot', 'box', 'checkpoint', 'dirt', 'enemy',
           'falling', 'flag', 'grass', 'laser', 'moving',
           'playerpos', 'shooter', 'spike', 'trampoline']

# Dictionary mapping keyboard letters to block types for quick placement
b_letters = {'a': 'aimbot',
             'B': 'box',
             'c': 'checkpoint',
             'd': 'dirt',
             'e': 'enemy',
             'f': 'falling',
             'G': 'flag',
             'g': 'grass',
             '-': 'laser',
             'm': 'moving',
             'P': 'playerpos',
             's': 'shooter',
             'S': 'spike',
             'T': 'trampoline'}

# List of keyboard letters available for block placement shortcuts
letter_list = ['a', 'B', 'c', 'd', 'e', 'f', 'G', 'g', '-', 'm', 'P', 's', 'S', 'T']

# Dictionary to store loaded and scaled block images for editor display
b_imgs = {}
# Function to load and scale block images for display in the editor
def nbi(name, w=1, h=1): # new block img
    # Load the block image from the assets folder
    img = pygame.image.load(f'../assets/img/blocks/{name}.png')
    # Scale the image to the appropriate tile size (width*TS, height*TS)
    img = pygame.transform.scale(img, (w*TS, h*TS))
    # Store the scaled image in the dictionary with the block name as key
    b_imgs.update({name: img})

# Load all block images, with special handling for differently sized blocks
for bn in b_names:
    # Check if this is a moving block which needs double width
    if bn == 'moving':
        # Load moving block with 2x width
        nbi(bn, 2)
    # For all other blocks, use standard 1x1 size
    else:
        # Load block with standard dimensions
        nbi(bn)


          
