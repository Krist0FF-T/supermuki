# Import sys module for system exit functionality
import sys
# Import pygame library for graphics and event handling
import pygame as pg
# Import constants, utility functions, and button modules for level selection interface
from . import consts, util, button


# Function to display level selection menu where players choose which level to play
def level_selection(surface, g):
    # Create rectangle for the quit/back button positioned in top-left corner
    button_quit_r = pg.Rect(50, 50, 160, 90)
    # Create surface for the quit button with same dimensions as rectangle
    button_quit_s = pg.Surface((button_quit_r.width, button_quit_r.height))

    # Define the width of level selection buttons in pixels
    lb_width = 120

    # 10 frame countdown after mouse key press
    # Initialize cooldown timer to prevent immediate clicking after opening menu
    cd = 10

    # Create rectangle for settings/restart button positioned in top-right corner
    sr_r = pg.Rect(consts.W-50-250, 50, 250, 90)
    # Create surface for the settings/restart button
    sr_s = pg.Surface((sr_r.width, sr_r.height))

    # Define the number of rows for level selection grid layout
    b_rows = 2
    # Define the number of columns for level selection grid layout
    b_cols = 5

    # Flag to control the level selection menu loop
    selecting_level = True
    # Main level selection loop that continues until a level is chosen or menu is exited
    while selecting_level:
        # Limit the menu to 60 frames per second for smooth performance
        consts.clock.tick(60)
        # Fill the screen with the game's GUI background color
        surface.fill(g.gui_rgb)
        # Get current mouse cursor position for button hover and click detection
        pos = pg.mouse.get_pos()

        # Check if cooldown timer is still active
        if cd > 0:
            # Decrement the cooldown timer each frame
            cd -= 1

        # Render the quit button with green color and hover effects
        button.green_button(button_quit_s, button_quit_r, pos)
        # Draw the quit button surface onto the screen at its position
        surface.blit(button_quit_s, button_quit_r)
        # Draw "Back" text centered on the quit button
        util.draw_text(
            surface, True, 40, "Back", "white",
            button_quit_r.centerx, button_quit_r.centery
        )

        # Render the settings/restart button with green color and hover effects
        button.green_button(sr_s, sr_r, pos)
        # Draw the settings/restart button surface onto the screen
        surface.blit(sr_s, sr_r)

        # Loop through each column of the level selection grid
        for i in range(b_cols):
            # Loop through each row of the level selection grid
            for y in range(b_rows):
                # Calculate the level number based on grid position (1-10 for 2x5 grid)
                num = i + (y * b_cols) + 1
                # Create rectangle for this level button at calculated grid position
                option_r = pg.Rect(
                    (140 * i) + 300,
                    (140 * y) + 280,
                    lb_width, lb_width
                )
                # Create surface for this level button with appropriate dimensions
                option_s = pg.Surface((
                    option_r.width, option_r.height
                ))

                # Fill the level button with green color as default state
                option_s.fill(consts.GREEN)
                # Check if mouse cursor is hovering over this level button
                if option_r.collidepoint(pos):
                    # Change to lighter green color when hovering
                    option_s.fill((120, 255, 120))
                    # Check if cooldown has expired and left mouse button is pressed
                    if cd <= 0 and pg.mouse.get_pressed()[0]:
                        # Change to dark gray color when button is being clicked
                        option_s.fill((50, 50, 50))
                        # Set the level to load as a string for file loading
                        g.level_to_load = f"{num}"
                        # Set the current level number in the game object
                        g.level = num
                        # Mark that a level has been selected
                        g.level_selected = True
                        # Exit the level selection loop
                        selecting_level = False

                # Draw the level button surface onto the screen at its position
                surface.blit((option_s), option_r)
                # Draw the level number centered on the button
                util.draw_text(surface, True, 50, str(num), "white",
                               option_r.centerx, option_r.centery)

        # Draw the main title "Level Selection" centered at the top of the screen
        util.draw_text(
            surface, True, 60,
            "Level Selection",
            consts.WHITE, consts.CX, 90
        )

        # Update the display to show all drawn elements
        pg.display.update()

        # Process all pygame events (keyboard, mouse, window close)
        for event in pg.event.get():
            # Check if the user clicked the X button to close the window
            if event.type == pg.QUIT:
                # Quit pygame and exit the program completely
                pg.quit()
                sys.exit()

            # Check if a mouse button was released (click completed)
            if event.type == pg.MOUSEBUTTONUP:
                # Check if the click was on the quit/back button
                if button_quit_r.collidepoint(pos):
                    # Mark that no level was selected
                    g.level_selected = False
                    # Exit the level selection loop
                    selecting_level = False
                    # Reset level to load to level 1 as default
                    g.level_to_load = "1"
