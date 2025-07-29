# Import pygame library for event handling and graphics functionality
import pygame as pg
# Import button, constants, and utility modules for menu functionality
from . import button, consts, util


# Function to display and handle the main menu where players choose single or multiplayer mode
def main_menu(surface, game):
    # Initialize option variable to track which game mode is selected (0=none, 1=single, 2=multiplayer)
    option = 0
    # Set the main title text to be displayed at the top of the menu
    text1 = 'Super Muki'
    # Define the current version number to display in the menu
    version = '1.5'
    # Flag to track whether a selection has been made to exit the menu loop
    selected = False

    # Create rectangle for the left button (1 Player) positioned on the left side of screen
    b1_r = pg.Rect(100, consts.CY, 400, 200)
    # Create surface for the left button with the same dimensions as its rectangle
    b1_s = pg.Surface((b1_r.width, b1_r.height))

    # Create rectangle for the right button (2 Player) positioned on the right side of screen
    b2_r = pg.Rect(consts.W-500, consts.CY, 400, 200)
    # Create surface for the right button using the left button's dimensions
    b2_s = pg.Surface((b1_r.width, b1_r.height))

    # Main menu loop that continues until a selection is made
    while not selected:
        # Limit the menu to 60 frames per second for smooth animation
        consts.clock.tick(60)
        # Get the current mouse cursor position for button hover detection
        pos = pg.mouse.get_pos()
        # Fill the screen with dark blue background color
        surface.fill((0, 0, 80))

        # Render the left button with green color and hover effects based on mouse position
        button.green_button(b1_s, b1_r, pos)
        # Render the right button with green color and hover effects based on mouse position
        button.green_button(b2_s, b2_r, pos)

        # Draw the left button surface onto the main screen at its rectangle position
        surface.blit(b1_s, b1_r)
        # Draw the right button surface onto the main screen at its rectangle position
        surface.blit(b2_s, b2_r)

        # Draw "1 Player" text centered on the left button
        util.draw_text(
            surface, True, 60, '1 Player',
            "white", b1_r.centerx, b1_r.centery
        )

        # Draw "2 Player" text centered on the right button
        util.draw_text(
            surface, True, 60, '2 Player',
            "white", b2_r.centerx, b2_r.centery
        )

        # Draw the main title "Super Muki" centered at the top of the screen
        util.draw_text(
            surface, True, 100, text1, "white",
            surface.get_width() // 2, 150
        )

        # Draw version information in the bottom-left corner of the screen
        util.draw_text(
            surface, False, 30, f'version: {version}',
            "white", 30, consts.H-60
        )

        # Update the display to show all drawn elements
        pg.display.update()

        # Process all pygame events (keyboard, mouse, window close)
        for event in pg.event.get():

            # Check if the user clicked the X button to close the window
            if event.type == pg.QUIT:
                # Set selected flag to exit menu loop
                selected = True
            # Check if a key was pressed down
            if event.type == pg.KEYDOWN:
                # Check if Escape key was pressed to exit menu
                if event.key == pg.K_ESCAPE:
                    # Set selected flag to exit menu loop
                    selected = True
                # Check if number 1 key was pressed to select single player
                if event.key == pg.K_1:
                    # Set option to 1 for single player mode
                    option = 1
                    # Set selected flag to exit menu loop
                    selected = True
                # Check if number 2 key was pressed to select multiplayer
                if event.key == pg.K_2:
                    # Set option to 2 for two player mode
                    option = 2
                    # Set selected flag to exit menu loop
                    selected = True

            # Check if a mouse button was released (button click completed)
            if event.type == pg.MOUSEBUTTONUP:
                # Check if the click was on the left button (1 Player)
                if b1_r.collidepoint(pos):
                    # Set option to 1 for single player mode
                    option = 1
                    # Set selected flag to exit menu loop
                    selected = True
                # Check if the click was on the right button (2 Player)
                if b2_r.collidepoint(pos):
                    # Set option to 2 for two player mode
                    option = 2
                    # Set selected flag to exit menu loop
                    selected = True

    # Store the selected number of players in the game object
    game.players = option
