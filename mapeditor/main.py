# Import pygame library with alias for graphics and input handling
import pygame as pg
# Import all variables and functions from the second module for block definitions
from second import *
# from os.path import exists
# from random import choice, randint

# Prompt user to enter filename for the level to edit or create
f_name = input('filename: ')
# Construct full file path for the level file in the levels directory
f_name = f'../levels/{f_name}.txt'

# Try to load an existing level file if it exists
try:
    # Initialize empty list to store the loaded level blocks
    blocks = []
    # Open the level file in read mode
    with open(f_name, 'r') as f:
        # Read all lines from the file into a list
        loaded = f.readlines()
        # Loop through each row (line) in the loaded data with its index
        for y, row in enumerate(loaded):
            # Initialize empty list for the current row of blocks
            therow = []
            # Loop through each character (column) in the row with its index
            for x, col in enumerate(row):
                # Add each character to the current row list
                therow.append(col)
            # Add the completed row to the main blocks list
            blocks.append(therow)

# If file doesn't exist or can't be loaded, create a new empty level
except:
    # Initialize empty list for creating new level from scratch
    blocks = []
    # Loop through each row index up to the defined number of rows
    for y in range(ROWS):
        # Initialize empty list for the current row
        row = []
        # Loop through each column index up to the defined number of columns
        for x in range(COLS):
            # Fill each position with '.' to represent empty space
            row.append('.')
        # Add newline character at the end of each row for proper file formatting
        row.append('\n')
        # Add the completed row to the main blocks list
        blocks.append(row)

# Create the main window/screen for the map editor with defined dimensions
screen = pg.display.set_mode((W, H))
# Set the window title to identify this as the map editor
pg.display.set_caption('MapMaker for Dungeon')

# Initialize horizontal scroll offset for panning the map view
scroll = 0
# Set default selected block type to 'g' (grass)
sel_letter = 'g'
# Set default selected block number index to 0 in the block list
sel_num = 0

# Function to save the current level layout to the file
def savetxt():
    # Open the level file in write mode to save changes
    with open(f_name, 'w') as f:
        # Loop through each row in the blocks grid
        for row in blocks:
            # Write all characters in the row to the file
            f.writelines(row)

# Function to display block selection menu and handle user input
def b_selection() -> int:
    # Flag to control the selection menu loop
    e = True
    # Initialize selection with current selected block number
    sel = sel_num
    # Main selection menu loop
    while e:
        # Get current mouse cursor position
        pos = pg.mouse.get_pos()
        # Limit frame rate to 30 FPS for the selection menu
        clock.tick(30)
        # Fill screen with dark blue background color
        screen.fill((0,0,50))
        
        # Loop through each available block type with its index
        for i, letter in enumerate(letter_list):
            # Get the image for this block type from the dictionary
            img = b_imgs[b_letters[letter]]
            # Scale the image to standard tile size for consistent display
            img = pg.transform.scale(img, (TS, TS))
            # Create rectangle for this block option positioned horizontally
            r = pg.Rect(i*80+100, 400, TS, TS)

            # Draw the block image at its position on screen
            screen.blit(img, (r.x, r.y))
            # Check if this block is currently selected
            if sel == i:
                # Draw red border around selected block to highlight it
                pg.draw.rect(screen, (255,0,0), r, 8)
            # Check if mouse cursor is over this block option
            if r.collidepoint(pos):
                # Check if left mouse button is pressed
                if pg.mouse.get_pressed()[0]:
                    # Set this block as the selected one
                    sel = i

        # Draw title text for the block selection menu
        mts(screen, True, 40, 'block selection', (255,255,255), CX, 100)

        # Update the display to show all drawn elements
        pg.display.update()

        # Process all pygame events for the selection menu
        for ev in pg.event.get():
            # Check if user clicked X to close window
            if ev.type == pg.QUIT: e = False
            # Check if a key was pressed
            if ev.type == pg.KEYDOWN:
                # Check if Escape key was pressed to cancel selection
                if ev.key == pg.K_ESCAPE: e = False
                # Check if Space key was pressed to confirm selection
                if ev.key == pg.K_SPACE:
                    # Return the currently selected block index
                    return sel

    # Return original selection if menu was cancelled
    return sel_num

# Flag to toggle grid display on/off
grid = False

# Main editor loop flag
run = True
# Main map editor loop
while run:
    # Get current mouse cursor position
    pos = pg.mouse.get_pos()
    # Limit frame rate to defined FPS for smooth performance
    clock.tick(FPS)
    # Fill screen with light blue background color
    screen.fill((100,180,240))

    # Clamp scroll to prevent scrolling too far right (positive values)
    if scroll > 0: scroll = 0
    # Clamp scroll to prevent scrolling too far left (beyond map boundary)
    if scroll < -4720: scroll = -4720

    # Calculate grid position based on mouse position and scroll offset
    sel_pos = [int((pos[0]-scroll)/TS), int((pos[1])/TS)]

    # Loop through each row and column in the blocks grid
    for y, row in enumerate(blocks):
        for x, col in enumerate(row):
            # Check if this position contains a valid block and is visible on screen
            if col in letter_list and -scroll-TS < x*TS < -scroll+W:
                # Get the image for this block type
                img = b_imgs[b_letters[col]]
                # Draw the block image at its world position adjusted for scroll
                screen.blit(img, (x*TS+scroll, y*TS))

    # Check if grid overlay should be displayed
    if grid:
        # Draw vertical grid lines
        for x in range(1, 21):
            # Draw horizontal grid lines
            for y in range(1, ROWS):
                # Adjust x position based on scroll offset
                x += int(-scroll/TS)
                # Calculate screen x position for vertical line
                tx = x*TS+scroll
                # Draw vertical grid line from top to bottom of screen
                pg.draw.line(screen, (0,0,0), (tx, 0), (tx, H))
                # Draw horizontal grid line across the screen width
                pg.draw.line(screen, (0,0,0), (0, y*TS), (W, y*TS))
    
    # Create preview image of currently selected block with transparency
    e = b_imgs[b_letters[sel_letter]].copy()
    # Set transparency to show where block would be placed
    e.set_alpha(80)
    # Draw preview block at mouse cursor position
    screen.blit(e, (sel_pos[0]*TS+scroll, sel_pos[1]*TS))

    # Display current cursor grid coordinates in top-left corner
    mts(screen, False, 30, f'{sel_pos[0]};{sel_pos[1]}', (255,255,255), 20, 20)

    # Update the display to show all drawn elements
    pg.display.update()

    # Get current state of all keyboard keys
    keys = pg.key.get_pressed()
    # Check if right arrow or D key is pressed to scroll right
    if keys[pg.K_RIGHT] or keys[pg.K_d]: scroll -= 20
    # Check if left arrow or A key is pressed to scroll left
    if keys[pg.K_LEFT]  or keys[pg.K_a]: scroll += 20

    # Get current state of all mouse buttons
    mb = pg.mouse.get_pressed()

    # left click: destroy
    # Check if left mouse button is pressed to remove blocks
    if mb[0]:
        # Set the block at cursor position to empty space
        blocks[sel_pos[1]][sel_pos[0]] = '.'

    # right click: place
    # Check if right mouse button is pressed to place blocks
    if mb[2]:
        # Set the block at cursor position to currently selected block type
        blocks[sel_pos[1]][sel_pos[0]] = sel_letter

    # Process all pygame events for the main editor
    for ev in pg.event.get():
        # Check if user clicked X to close window
        if ev.type == pg.QUIT:
            # Exit the main editor loop
            run = False

        # Check if a key was pressed down
        if ev.type == pg.KEYDOWN:
            # Check if Escape key was pressed to exit editor
            if ev.key == pg.K_ESCAPE:
                # Exit the main editor loop
                run = False

            # Check if Space key was pressed to open block selection menu
            if ev.key == pg.K_SPACE:
                # Call block selection function and update selected block
                sel_num = b_selection()
                # Try to update selected letter based on new selection
                try:
                    # Get the letter corresponding to the selected block index
                    sel_letter = letter_list[sel_num]
                # Handle any index errors gracefully
                except Exception:
                    # Continue with previous selection if error occurs
                    pass

            # Check if G key was pressed to toggle grid display
            if ev.key == pg.K_g:
                # Toggle the grid display flag
                grid = not grid

            # Check if X key was pressed to pick block type from cursor position
            if ev.key == pg.K_x:
                # Get the block type at current cursor position
                e = blocks[sel_pos[1]][sel_pos[0]]
                # Check if it's a valid block type
                if e in letter_list:
                    # Set this block type as currently selected
                    sel_letter = e

            # Check if S key was pressed to save the level
            if ev.key == pg.K_s:
                # Call the save function to write level to file
                savetxt()

            # Check if F11 key was pressed to toggle fullscreen mode
            if ev.key == pg.K_F11:
                # Toggle between windowed and fullscreen display
                pg.display.toggle_fullscreen()

        # Check if mouse wheel or button was pressed
        if ev.type == pg.MOUSEBUTTONDOWN:
            # Check if mouse wheel scrolled up and not at first block
            if ev.button == 4 and sel_num > 0:
                # Move to previous block in selection list
                sel_num -= 1
                # Update selected letter to match new selection
                sel_letter = letter_list[sel_num]

            # Check if mouse wheel scrolled down and not at last block
            if ev.button == 5 and sel_num < len(letter_list)-1:
                # Move to next block in selection list
                sel_num += 1
                # Update selected letter to match new selection
                sel_letter = letter_list[sel_num]

# Save the level one final time before exiting
savetxt()

# Clean up and quit pygame
pg.quit()
