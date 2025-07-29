# Import random module for random number generation used in game mechanics
import random
# Import pygame library for graphics, sound, and input handling
import pygame as pg
# Import json module for loading game configuration from config file
import json
# Import sys module for system exit functionality
import sys
# Import math functions for trigonometric calculations in movement and physics
from math import sin, cos, atan2, hypot

# Import level selection menu functionality
from scripts.level_selection import level_selection
# Import main menu functionality for player count selection
from scripts.main_menu import main_menu
# Import constants, button utilities, and general utility functions
from scripts import consts, button, util
# Import asset manager for loading and managing game assets
from scripts.assets import asset_manager

# Open and load game configuration from JSON file
with open("config.json", "r") as f:
    # Parse the JSON configuration data
    config = json.load(f)
    # Extract fullscreen setting from configuration
    fullscreen = config["auto_fullscreen"]
    # Extract vsync setting from configuration
    vsync = config["vsync"]

# Create the main game window with specified dimensions and vsync setting
screen = pg.display.set_mode((consts.W, consts.H), vsync=vsync)
# Set the window title to identify the game
pg.display.set_caption("SuperMuki")

# Load all player sprite images using the asset manager
asset_manager.load_player_imgs("player")


# Define the main Game class that manages game state and settings
class Game:
    # Initialize the game with default settings and state variables
    def __init__(self):
        # Set the background color for GUI elements (dark blue)
        self.gui_rgb = (0, 0, 80)
        # Define the total number of levels available in the game
        self.num_of_levels = 10
        # Set the current level number (starting at level 1)
        self.level = 1
        # Flag to indicate if a level should be loaded from the level selection menu
        self.load_level_bool = False
        # Flag to track if a level has been selected in the level selection menu
        self.level_selected = False

        # Set the number of players (1 or 2 player mode)
        self.players = 1
        # Flag to temporarily stop player movement (used during transitions)
        self.stop_player_move = False
        # Store the respawn coordinates where players will revive after death
        self.respawn_point = (0.0, 0.0)

        # Setting to enable/disable player sprite rotation during jumps
        self.flip_when_jump = True
        # Setting to show/hide death counter display
        self.show_deaths = True

        # Cheat mode flag that allows players to fly through levels
        self.flying = False

    # Method to reset the game timer (currently not used in main game)
    def reset_timer(self):
        # Reset timer values to zero (milliseconds, seconds, minutes)
        self.t_mval, self.t_sec, self.t_min = 0, 0, 0

    # Method to reset death count for all players and respawn them
    def reset_deaths(self):
        # Loop through all active players
        for player in players:
            # Respawn the player at the current respawn point
            player.respawn()
            # Reset their death counter to zero
            player.deaths = 0

    # Method to display and handle the color customization menu for players
    def color_selection(self):
        # Flag to control the color selection menu loop
        c_s = True
        # Define color bar lines for player 1 (RGB sliders)
        lines = [
            ["red", 200, 300, 450],
            ["green", 200, 410, 450],
            ["blue", 200, 520, 450]
        ]

        # Check if this is a 2-player game to add color bars for player 2
        if game.players == 2:
            # Add red color bar for player 2 on the right side of screen
            lines.append(["red",   consts.W-450, 300, consts.W-200])
            # Add green color bar for player 2 on the right side of screen
            lines.append(["green", consts.W-450, 410, consts.W-200])
            # Add blue color bar for player 2 on the right side of screen
            lines.append(["blue",  consts.W-450, 520, consts.W-200])

        # Create list of color control buttons for player 1 (RGB sliders)
        c_b1 = [button.p1_red, button.p1_green, button.p1_blue]
        # Create list of color control buttons for player 2 (RGB sliders)
        c_b2 = [button.p2_red, button.p2_green, button.p2_blue]

        # Get rectangle reference for the confirmation button
        confirm_r = button.confirm_c.rect
        # Create surface for the confirmation button with matching dimensions
        confirm_s = pg.Surface((confirm_r.width, confirm_r.height))

        # Main color selection menu loop
        while c_s:
            # Limit frame rate to target FPS for smooth performance
            consts.clock.tick(consts.FPS)
            # Fill screen with dark gray background color
            screen.fill((50, 50, 50))
            # Get current mouse cursor position for button interaction
            pos = pg.mouse.get_pos()
            # Render the confirmation button with gray color and hover effects
            button.colored_b(confirm_s, confirm_r, [80, 80, 80], pos)
            # Draw the confirmation button surface onto the screen
            screen.blit(confirm_s, confirm_r)
            # Draw "Done" text centered on the confirmation button
            util.draw_text(
                screen, True, 30, "Done", "white",
                confirm_r.centerx, confirm_r.centery
            )

            # Draw color slider lines for RGB color selection
            for li in lines:
                # Draw horizontal line for each color component (R, G, or B)
                pg.draw.line(screen, li[0], [li[1], li[2]], [
                    li[3], li[2]], 7)

            # Draw color control buttons for player 1
            for bu1 in c_b1:
                # Draw each RGB slider button for player 1
                bu1.draw(screen)
            # Check if there are 2 players to draw player 2's controls
            if game.players == 2:
                # Draw color control buttons for player 2
                for bu2 in c_b2:
                    # Draw each RGB slider button for player 2
                    bu2.draw(screen)

            # Loop through RGB color components (red, green, blue)
            for i in range(3):
                # Constrain player 1's color slider to stay within left boundary
                if c_b1[i].rect.left < 200:
                    c_b1[i].rect.left = 200
                # Constrain player 1's color slider to stay within right boundary
                if c_b1[i].rect.right > 450:
                    c_b1[i].rect.right = 450

                # Apply constraints for player 2's sliders if in 2-player mode
                if game.players == 2:
                    # Constrain player 2's color slider to stay within left boundary
                    if c_b2[i].rect.left < consts.W-450:
                        c_b2[i].rect.left = consts.W-450
                    # Constrain player 2's color slider to stay within right boundary
                    if c_b2[i].rect.right > consts.W-200:
                        c_b2[i].rect.right = consts.W-200

                # Calculate player 1's color value based on slider position (0-250 range)
                player1.color[i] = c_b1[i].rect.centerx - 200
                # Calculate player 2's color value if in 2-player mode
                if game.players == 2:
                    player2.color[i] = c_b2[i].rect.centerx - (consts.W-450)

            # Regenerate player 1's sprite images with new color
            player1.images = []
            # Loop through each base player sprite image
            for c_img in asset_manager.player_images:
                # Apply color swap to the sprite using the new color values
                p_img = util.palette_swap(c_img, c_img.get_at(
                    (0, 0)), player1.color).convert()
                # Set black as transparent color for proper sprite rendering
                p_img.set_colorkey((0, 0, 0))
                # Add the recolored sprite to player 1's image list
                player1.images.append(p_img)

            # Generate player 2's sprite images if in 2-player mode
            if game.players == 2:
                # Clear player 2's current sprite images
                player2.images = []
                # Loop through each base player sprite image
                for c_img in asset_manager.player_images:
                    # Apply color swap to the sprite using player 2's color values
                    p_img = util.palette_swap(c_img, c_img.get_at(
                        (0, 0)), player2.color).convert()
                    # Set black as transparent color for proper sprite rendering
                    p_img.set_colorkey((0, 0, 0))
                    # Add the recolored sprite to player 2's image list
                    player2.images.append(p_img)

            # Create preview image of player 1's sprite scaled to 80x80 pixels
            p1_pv_image = pg.transform.scale(player1.images[2], (80, 80))
            # Get rectangle for player 1's preview image
            p1_pv_rect = p1_pv_image.get_rect()
            # Position player 1's preview on the left side of screen
            p1_pv_rect.center = 350, 120

            # Create preview image of player 2's sprite scaled to 80x80 pixels
            p2_pv_image = pg.transform.scale(player2.images[2], (80, 80))
            # Get rectangle for player 2's preview image
            p2_pv_rect = p2_pv_image.get_rect()
            # Position player 2's preview on the right side of screen (note: should be consts.W instead of util.W)
            p2_pv_rect.center = util.W - 350, 120

            # Draw player 1's sprite preview on screen
            screen.blit((p1_pv_image), p1_pv_rect)
            # Draw player 2's sprite preview if in 2-player mode
            if game.players == 2:
                screen.blit((p2_pv_image), p2_pv_rect)

            # Display player 1's current RGB color values below their preview
            util.draw_text(
                screen, True, 30, str(player1.color),
                "white", p1_pv_rect.centerx, consts.H - 100
            )

            # Display player 2's current RGB color values if in 2-player mode
            if game.players == 2:
                util.draw_text(
                    screen, True, 30, str(player2.color),
                    "white", p2_pv_rect.centerx, consts.H - 100
                )

            # Update the display to show all color selection elements
            pg.display.update()

            # Check if left mouse button is being held down for dragging sliders
            if pg.mouse.get_pressed()[0]:
                # Handle dragging for player 1's color sliders
                for bu in c_b1:
                    # Create expanded hit area around each slider button for easier dragging
                    if pg.Rect(
                        bu.rect.x-25,
                        bu.rect.y-25,
                        bu.rect.width+50,
                        bu.rect.height+50
                    ).collidepoint(pos):
                        # Move slider button to follow mouse x-position
                        bu.rect.centerx = pos[0]
                    # Ensure slider doesn't go past left boundary
                    if bu.rect.left < 200:
                        bu.rect.left = 200
                    # Ensure slider doesn't go past right boundary
                    if bu.rect.right > 450:
                        bu.rect.right = 450

                # Handle dragging for player 2's color sliders if in 2-player mode
                if game.players == 2:
                    for bu in c_b2:
                        # Create expanded hit area around each slider button for easier dragging
                        if pg.Rect(
                            bu.rect.x - 20,
                            bu.rect.y - 20,
                            bu.rect.width + 40,
                            bu.rect.height + 40
                        ).collidepoint(pos):
                            # Move slider button to follow mouse x-position
                            bu.rect.centerx = pos[0]

                        # Ensure player 2's slider doesn't go past left boundary
                        if bu.rect.left < consts.W - 450:
                            bu.rect.left = consts.W - 450

                        # Ensure player 2's slider doesn't go past right boundary
                        if bu.rect.right > consts.W - 200:
                            bu.rect.right = consts.W - 200

            # Process all pygame events for the color selection menu
            for event in pg.event.get():
                # Check if user clicked X to close window
                if event.type == pg.QUIT:
                    # Quit pygame and exit program
                    pg.quit()
                    sys.exit()
                # Check if a key was pressed
                if event.type == pg.KEYDOWN:
                    # Check if Space or Escape key was pressed to exit color selection
                    if event.key in [pg.K_SPACE, pg.K_ESCAPE]:
                        # Set flag to exit color selection loop
                        c_s = False

                # Check if mouse button was clicked
                if event.type == pg.MOUSEBUTTONDOWN:
                    # Check if click was on the confirmation button
                    if button.confirm_c.rect.collidepoint(pos):
                        # Set flag to exit color selection loop
                        c_s = False


# Create the main game instance with all settings and state
game = Game()


# Function to display and handle the pause menu when game is paused
def pause():
    # reset_time_b = Button(0, 100, "simple_b2.png", 12)

    # Get rectangle reference for the resume button
    resume_r = button.resume_button.rect
    # Create surface for the resume button with matching dimensions
    resume_s = pg.Surface((resume_r.width, resume_r.height))

    # Get rectangle reference for the quit button
    quit_r = button.quit_button.rect
    # Create surface for the quit button with matching dimensions
    quit_s = pg.Surface((quit_r.width, quit_r.height))
    # Flag to track if user wants to return to main menu
    mm = False  # enter main menu

    # Flag to control the pause menu loop
    paused = True
    # Main pause menu loop
    while paused:
        # Get current mouse cursor position for button interaction
        pos = pg.mouse.get_pos()
        # Limit frame rate to target FPS
        consts.clock.tick(consts.FPS)
        # Fill screen with the game's GUI background color
        screen.fill(game.gui_rgb)

        # draw buttons
        # Draw the load level button
        button.load_lvl_b.draw(screen)
        # Draw the color selection button
        button.color_s_b.draw(screen)

        # Draw the main menu button
        button.mainm_b.draw(screen)

        # Render the resume button with green color and hover effects
        button.green_button(resume_s, resume_r, pos)
        # Draw the resume button surface onto the screen
        screen.blit(resume_s, resume_r)

        # Render the quit button with green color and hover effects
        button.green_button(quit_s, quit_r, pos)
        # Draw the quit button surface onto the screen
        screen.blit(quit_s, quit_r)

        # draw text
        # Draw "Paused!" title text centered at the top
        util.draw_text(screen, True, 100, "Paused!",
                       "white", consts.CX, 150)
        # Draw "Resume (C)" text on the resume button
        util.draw_text(
            screen, True, 45, "Resume (C)", "white",
            button.resume_button.rect.centerx,
            button.resume_button.rect.centery
        )
        # Draw "Quit (Q)" text on the quit button
        util.draw_text(
            screen, True, 45, "Quit (Q)", "white",
            button.quit_button.rect.centerx, button.quit_button.rect.centery
        )

        # Update the display to show all pause menu elements
        pg.display.update()

        # events
        # Process all pygame events for the pause menu
        for event in pg.event.get():
            # Check if user clicked X to close window
            if event.type == pg.QUIT:
                # Quit pygame and exit program
                pg.quit()
                sys.exit()
            # Check if a key was pressed down
            if event.type == pg.KEYDOWN:
                # Check if Q key was pressed to quit game
                if event.key == pg.K_q:
                    # Quit pygame and exit program
                    pg.quit()
                # Check if Escape or C key was pressed to resume game
                if event.key == pg.K_ESCAPE or event.key == pg.K_c:
                    # Exit pause menu and resume game
                    paused = False

            # Check if a mouse button was released (click completed)
            if event.type == pg.MOUSEBUTTONUP:
                # Check if click was on resume button
                if resume_r.collidepoint(pos):
                    # Exit pause menu and resume game
                    paused = False
                # Check if click was on quit button
                if quit_r.collidepoint(pos):
                    # Quit pygame and exit program
                    pg.quit()
                    sys.exit()
                # Check if click was on load level button
                if button.load_lvl_b.rect.collidepoint(pos):
                    # Set flag to load level selection menu
                    game.load_level_bool = True
                    # Exit pause menu
                    paused = False
                # Check if click was on color selection button
                if button.color_s_b.rect.collidepoint(pos):
                    # Open color selection menu
                    game.color_selection()
                # Check if click was on main menu button
                if button.mainm_b.rect.collidepoint(pos):
                    # Exit pause menu and set flag to return to main menu
                    paused = False
                    mm = True

    # Check if user chose to return to main menu
    if mm:
        # Show main menu to select number of players
        main_menu(screen, game)
        # Adjust player list based on selected player count
        if game.players == 2:
            # Add player 2 if not already in the list for 2-player mode
            if len(players) < 2:
                players.append(player2)
        else:
            # Clear player list and add only player 1 for single-player mode
            players.clear()
            players.append(player1)

        # Reset death counts for all active players
        for p in players:
            p.deaths = 0
        # Open color selection menu for player customization
        game.color_selection()
        # Reset level selection flag
        game.level_selected = False
        # Show level selection menu
        level_selection(screen, game)

        # Load the selected level or default to level 1
        if game.level_selected:
            # Load the level chosen by the player
            load_level(game.level)
        else:
            # Load level 1 as default if no level was selected
            load_level(1)


# Function to draw game statistics and information on the screen during gameplay
def draw_stats():
    # Draw current level number in the top-left corner
    util.draw_text(screen, False, 30, f"level {game.level}", "white", 15, 15)

    # Check if fly mode (cheat) is enabled and display indicator
    if game.flying:
        # Draw "fly" text centered at the top to indicate cheat mode is active
        util.draw_text(screen, True, 20, "fly", "white", consts.CX, 30)

    # Check if death counter display is enabled
    if game.show_deaths:
        # Draw "deaths" label in the top-right area
        util.draw_text(screen, True, 30, "deaths", "white", consts.W - 80, 30)
        # Handle single-player mode death counter
        if game.players == 1:
            # Display player 1's death count using their custom color
            util.draw_text(
                screen, True, 30, f"{player1.deaths}",
                player1.color, consts.W - 80, 90
            )

        # Handle two-player mode death counters
        elif game.players == 2:
            # Display death count for each player
            for player in players:
                # Display each player's death count using their custom color, positioned by player number
                util.draw_text(
                    screen, True, 30, f"{player.deaths}",
                    player.color, consts.W-200+(80*player.num), 90
                )


# Define the Camera class for managing viewport and following players
class Camera:
    # Initialize camera with default position and targeting values
    def __init__(self):
        # Current camera x position (horizontal offset)
        self.x = 0
        # Target x position the camera should move toward
        self.target_x = 0
        # Floating point x position for smooth interpolation
        self.float_x = 0

        # Current camera y position (vertical offset)
        self.y = 0
        # Target y position the camera should move toward
        self.target_y = 0
        # Floating point y position for smooth interpolation
        self.float_y = 0

        # Reference to preferred player for camera focus when players are far apart
        self.preferred: Player | None = None

    # Method to update camera position based on player positions
    def update(self):
        # Handle camera positioning for 2-player mode
        if game.players == 2:
            # Calculate target position as midpoint between both players
            self.target_x = - (
                player1.rect.centerx + player2.rect.centerx
            ) / 2 + consts.CX

            # Calculate distance between players
            distance = abs(player1.rect.centerx - player2.rect.centerx)
            # Check if players are too far apart for good camera framing
            far_apart = distance > consts.W - 300

            # If players are far apart and there's a preferred player, focus on them
            if far_apart and self.preferred:
                # Center camera on the preferred player instead of midpoint
                self.target_x = -self.preferred.rect.centerx + consts.CX

            # self.target_y = -(
            #     (player1.rect.centery + player2.rect.centery) / 2
            # ) + consts.CY

        # Handle camera positioning for single-player mode
        elif game.players == 1:
            # Center camera on player 1
            self.target_x = -player1.rect.centerx + consts.CX
            # self.target_y = -player1.rect.centery + CY

        # Smoothly interpolate camera x position toward target (5% per frame)
        self.float_x += (self.target_x - self.float_x)*0.05
        # Convert to integer pixel position
        self.x = int(self.float_x)

        # Smoothly interpolate camera y position toward target (5% per frame)
        self.float_y += (self.target_y - self.float_y)*0.05
        # Convert to integer pixel position
        self.y = int(self.float_y)

        # Prevent camera from scrolling too far to the right (past right edge of level)
        if self.x > 0:
            # Clamp camera to right boundary
            self.x = 0

        # Prevent camera from scrolling too far to the left (past left edge of level)
        if self.x < -4720:
            # Clamp camera to left boundary (level width limit)
            self.x = -4720


# Create the main camera instance for the game
cam = Camera()

# Player movement flags for player 1 (left and right movement)
left,  right = False, False
# Player movement flags for player 2 (left and right movement)
left2, right2 = False, False


# Define the Player class for character management and physics
class Player:
    # Initialize a new player with specified number (1 or 2)
    def __init__(self, num):

        # graphical -----
        # Initialize empty list to store player sprite images
        self.images = []
        # Copy all base player images from asset manager
        for img in asset_manager.player_images:
            # Add each sprite frame to the player's image list
            self.images.append(img)

        # Current animation frame index (1-3 for different poses)
        self.frame_index = 1
        # Animation cooldown timer for controlling frame rate
        self.animation_cd = 0

        # Player's custom RGB color values [red, green, blue]
        self.color = [255, 0, 0]
        # Flag for horizontal sprite flipping based on direction
        self.flip = False
        # Current rotation angle for jump animation
        self.rotation = 0
        # Flag indicating if player sprite is currently rotating
        self.rotating = False

        # logical -------
        # Player number (1 or 2) for identification
        self.num = num
        # Flag indicating if player is "able to jump" (on ground)
        self.atj = False
        # Rectangle for collision detection and positioning
        self.rect = self.images[0].get_rect()
        # Direction player is facing (1 = right, -1 = left)
        self.direction = 1

        # - movement
        # Horizontal movement speed in pixels per frame
        self.speed = consts.PLAYER_SPEED
        # Horizontal knockback velocity from collisions
        self.knockback = 0
        # Flag indicating if jump input is being held
        self.jump = False
        # Vertical velocity for gravity and jumping
        self.vel_y = 0

        # - alive
        # Flag indicating if player is currently alive
        self.alive = True
        # Counter for number of times player has died
        self.deaths = 0

    # Method to update player state and handle basic physics
    def update(self):
        # Set sprite flip based on movement direction (left = flipped)
        self.flip = (self.direction == -1)

        # Check if alive player has fallen below the level boundary
        if self.rect.bottom > consts.ROW*consts.TS and self.alive:
            # Kill the player for falling out of bounds
            self.kill()
            # Clamp position to bottom boundary
            self.rect.bottom = consts.ROW * consts.TS

        # Check if dead player has fallen far enough to respawn
        if self.rect.top > consts.ROW*consts.TS and not self.alive:
            # Respawn the player at the respawn point
            self.respawn()

        # Prevent player from moving past left edge of level
        if self.rect.left < 0:
            # Clamp position to left boundary
            self.rect.left = 0

        # Prevent player from moving past right edge of level
        if self.rect.right > 6000:
            # Clamp position to right boundary (level width limit)
            self.rect.right = 6000

    def move(self, left, right):
        dx = 0
        dy = 0

        if self.alive and left and not right:
            cam.preferred = self
            dx = -self.speed
            self.direction = -1

        if self.alive and right and not left:
            cam.preferred = self
            dx = self.speed
            self.direction = 1

        if self.jump and (game.flying or self.atj):
            self.vel_y = -10
            self.rotating = True
            # print("e")
            self.jump = False

        if left or right and self.atj:
            self.animation_cd += 1
            if self.animation_cd >= 7:
                e = {1: 2, 2: 1, 3: 1}
                self.frame_index = e[self.frame_index]
                self.animation_cd = 0
        else:
            self.frame_index = 3

        if (self.rotating and game.flip_when_jump) or not self.alive:
            self.rotation -= 15
            # print("rotating")
            if abs(self.rotation) > 355:
                self.rotation = 0
                self.rotating = False

        dy += self.vel_y
        dx += self.knockback
        now_on_ground = False

        for block in collideblocks:
            if not self.alive:
                break

            if block[2] == "moving":
                if block[0].colliderect(
                    self.rect.x + dx, self.rect.y + dy + 10,
                    self.rect.width, self.rect.height
                ) and self.vel_y > -1:
                    if self.vel_y > 0:
                        self.vel_y = 0
                        self.atj = True
                        now_on_ground = True
                        dy = block[0].top - self.rect.bottom

                    dx = block[3]["speed"] * block[3]["direction"]

            if block[2] in solid_blocks:
                if block[0].colliderect(
                    self.rect.x + dx, self.rect.y,
                    self.rect.width, self.rect.height
                ):
                    if block[2] == "box":  # and self.atj:
                        dx = int(dx*0.3)
                        x_collide = False
                        for col_block in blocks:
                            if col_block != block:
                                if col_block[0].colliderect(
                                    block[0][0] + dx, block[0][1],
                                    consts.TS, consts.TS
                                ) or block[0].x < 0:
                                    x_collide = True

                        if x_collide:
                            dx = 0
                        # block[0].x += dx
                        block[3]["dx"] += dx

                    else:
                        dx = 0
                    self.knockback = 0
                if block[0].colliderect(
                    self.rect.x, self.rect.y + dy,
                    self.rect.width, self.rect.height
                ):
                    # if self.vel_y <= 0:
                    if block[0].bottom < self.rect.bottom:
                        self.vel_y = 0
                        dy = block[0].bottom - self.rect.top
                        if self.atj and self.alive:
                            self.kill()

                    else:
                        if block[2] == "falling":
                            block[3]["state"] = "fall"

                        self.vel_y = 0
                        now_on_ground = True
                        self.atj = True
                        dy = block[0].top - self.rect.bottom
                        self.rotating = False
                        self.rotation = 0

                    # cam.x += 300

        if abs(self.vel_y) >= 5:
            self.atj = False

        self.rect.x += dx
        self.rect.y += dy

        if not now_on_ground:
            self.vel_y += consts.GRAVITY

    def kill(self):
        if not self.alive:
            return

        asset_manager.get_sound("enemy_hit.wav").play()
        self.alive = False
        self.vel_y = -12

    def respawn(self):
        self.alive = True
        self.rotating = False
        self.rotation = 0
        self.vel_y = 0
        self.rect.topleft = game.respawn_point

    def velrect(self):
        return pg.Rect(
            self.rect.x, self.rect.y + self.vel_y,
            self.rect.width, self.rect.height
        )

    def draw(self):
        c_img = self.images[self.frame_index-1]
        if self.rect.bottom < 0:
            fallpos_image = c_img.copy()
            fallpos_image.set_alpha(80)
            screen.blit(
                pg.transform.flip(fallpos_image, self.flip, False),
                (self.rect.x + cam.x, 30)
            )

        if game.flip_when_jump:
            img_to_blit = pg.transform.rotate(c_img, self.rotation)

        else:
            img_to_blit = c_img

        # screen.blit(flip(img_to_blit, self.flip),
        #             (self.rect.x+cam.x, self.rect.y+cam.y))

        flipped = pg.transform.flip(img_to_blit, self.flip, False)

        # if not self.alive:
        #     flipped = flip_ver(flipped, True)

        rect = flipped.get_rect()
        rect.centerx = self.rect.centerx + cam.x
        rect.centery = self.rect.centery + cam.y
        screen.blit(flipped, rect)


solid_blocks = ["grass", "dirt", "shooter", "box", "falling"]
moving_blocks = ["moving", "enemy"]

collideblocks = []
reset_blocks = []

blocks = []
bg_blocks = []
bullets = []
lasers = []


def draw_bullets():
    for b in bullets:
        if -cam.x-100 < b[0][0] < -cam.x+100+consts.W:
            pg.draw.circle(screen, (0, 0, 255),
                           (b[0][0]+cam.x, b[0][1]+cam.y), 10)


def update_bullets():
    for b in bullets:
        b[0][0] += 7 * b[1]
        b[0][1] += 7 * b[2]
        for p in players:
            if p.rect.colliderect(b[0][0]-10, b[0][1]-10, 20, 20):
                p.kill()
                # p.deaths += 1
                # game_over(f"P{p.num} was pierced by a bullet")

        if consts.COL*consts.TS < b[0][0] < 0:
            bullets.remove(b)
        for block in collideblocks:
            if (
                block[2] not in ["shooter", "aimbot"] and
                block[0].colliderect(b[0][0]-10, b[0][1]-10, 20, 20)
            ):
                if b in bullets:
                    bullets.remove(b)


main_menu(screen, game)

player1 = Player(1)
player2 = Player(2)
players = [player1]
if game.players == 2:
    players.append(player2)

bg_lines = []
for i in range(22):
    i2 = i*4
    e = consts.W/25
    x = i2*e
    bg_lines.append([[x-consts.H, 0], [x, consts.H]])


def draw_bg_lines():
    bg_c = consts.bg_color
    color = (bg_c[0]+7, bg_c[1]+7, bg_c[2]+10)
    camx = cam.x*0.5
    camy = cam.y*0.5
    for line in bg_lines:
        if -camx-consts.W-consts.H < line[0][0]-consts.W < -camx:
            pg.draw.line(
                screen, color,
                (line[0][0]+camx, line[0][1]+camy),
                (line[1][0]+camx, line[1][1]+camy),
                40
            )


def add_bg_block(x, y, name):
    img = asset_manager.get_image(f"bg_blocks/{name}.png").convert()
    img.set_colorkey("black")

    image = pg.transform.scale(img, (consts.TS, consts.TS))

    rect = image.get_rect()
    rect.topleft = x*consts.TS, y*consts.TS
    bg_block = [rect, image, name]
    bg_blocks.append(bg_block)


def add_block(x, y, name, properties={}):
    img = asset_manager.get_image(f"blocks/{name}.png").convert_alpha()

    h = 1
    w = 2 if name == "moving" else 1

    image = pg.transform.scale(img, (consts.TS*w, consts.TS*h))

    rect = image.get_rect()
    rect.topleft = x*consts.TS, y*consts.TS
    block = [rect, image, name, properties]
    blocks.append(block)

    if name in solid_blocks or name in ["moving", "falling", "box"]:
        collideblocks.append(block)


def load_level(num, reload=False):
    if reload:
        for p in players:
            p.rect.topleft = game.respawn_point

    if game.level > game.num_of_levels:
        level_selection(screen, game)
        return

    blocks.clear()
    bullets.clear()
    collideblocks.clear()
    if not reload:
        bg_blocks.clear()
    fileName = f"assets/levels/{num}.txt"

    try:
        with open(fileName, "r") as f:
            tilemap = f.readlines()
    except Exception:
        load_level(1, reload)
        return

    lasers.clear()

    # place blocks
    for i, row in enumerate(tilemap):
        for j, col in enumerate(row):
            if col == ".":
                continue

            if col == "P" and not reload:
                game.stop_player_move = True
                game.respawn_point = j*consts.TS, i*consts.TS
                for p in players:
                    p.rect.topleft = game.respawn_point

            elif col == "B":
                add_block(j, i, "box", {"vel_y": 0, "dx": 0})
            elif col == "G":
                add_block(j, i, "flag")
            elif col == "S":
                add_block(j, i, "spike")
            elif col == "T":
                add_block(j, i, "trampoline")
            elif col == "m":
                add_block(j, i, "moving",  {"speed": 3, "direction": 1})
            elif col == "e":
                add_block(j, i, "enemy", {
                    "speed": 3,
                    "direction": 1,
                    "cd": 0,
                    "frame_index": 0
                })
            elif col == "s":
                add_block(j, i, "shooter", {"cooldown": 12})

            elif col == "a":
                add_block(j, i, "aimbot", {"cd": 12, "d": [1, 1]})

            elif col == "-":
                lasers.append([
                    [j*consts.TS, i*consts.TS+30],
                    [(j+1)*consts.TS, i*consts.TS+30]
                ])

            elif col == "g":
                add_block(j, i, "grass")
                if not reload:
                    if i > 0 and tilemap[i-1][j] == ".":
                        rn = random.random()
                        if rn < 0.1:
                            add_bg_block(j, i-1,   "grass")
                        elif rn < 0.2:
                            add_bg_block(j, i-1, "flower")
                        # elif rn < 0.3:
                        #     addBgBlock(j, i-1, "smiley")

            elif col == "d":
                add_block(j, i, "dirt")
            elif col == "f":
                add_block(j, i, "falling", {
                    "vel_y": 0,
                    "state": "fly",
                    "pos": i*consts.TS,
                    "cd": 0
                })
            elif col == "c":
                add_block(j, i, "checkpoint", {"status": "inactive"})


def draw_blocks():
    def on_screen(x):
        return -cam.x - 100 < x < -cam.x + 100 + consts.W

    for b in blocks:
        if not on_screen(b[0].centerx):
            continue

        if b[2] == "enemy":
            b[3]["cd"] += 1
            if b[3]["cd"] > 20:
                if b[3]["frame_index"] == 0:
                    b[3]["frame_index"] = 1
                else:
                    b[3]["frame_index"] = 0

                i = b[3]["frame_index"] + 1
                img = asset_manager.get_image(f"blocks/enemy/{i}.png")
                b[1] = pg.transform.scale(img, (consts.TS, consts.TS))
                b[3]["cd"] = 0

        elif b[2] == "checkpoint":
            s = b[3]["status"]
            img = asset_manager.get_image(f"blocks/checkpoint/{s}.png")
            b[1] = pg.transform.scale(img, (consts.TS, consts.TS))

        screen.blit(b[1], (b[0][0] + cam.x, b[0][1]+cam.y))

    for bg_b in bg_blocks:
        if not on_screen(bg_b[0].centerx):
            continue

        screen.blit(
            bg_b[1],
            (bg_b[0][0] + cam.x, bg_b[0][1]+cam.y),
            special_flags=pg.BLEND_ALPHA_SDL2
        )


def update_blocks():
    for block in blocks:
        update_block(block)

    for block in blocks:
        if block[2] == "box":
            block[3]["dx"] = 0


def update_block(block):
    rect, _, name, props = block
    if name in moving_blocks:
        # can the enemy walk forward (able to move)
        atm = False
        rect.x += props["speed"] * props["direction"]
        for s_block in blocks:
            if (
                s_block == block or
                s_block[2] not in (solid_blocks + ["enemy", "moving"]) or
                s_block[2] == "falling"
            ):
                continue

            if rect.colliderect(s_block[0]):
                props["direction"] *= -1

            if name == "enemy":
                if s_block[0].collidepoint(
                    rect.centerx + 20*props["direction"],
                    rect.bottom + 10
                ):
                    atm = True

        if name == "enemy":
            if not atm:
                props["direction"] *= -1

            for p in players:
                if not (p.alive and rect.colliderect(p.velrect())):
                    continue

                if p.vel_y > 1:
                    p.vel_y = -10
                    p.rotating = True
                    asset_manager.get_sound("enemy_hit.wav").play()

                    if block in blocks:
                        blocks.remove(block)

                else:
                    p.kill()

    elif name == "shooter":
        props["cooldown"] -= 1

        if (
            props["cooldown"] <= 0 and
            (-cam.x-100 < rect.centerx < -cam.x+100+consts.W)
        ):
            bullets.append([list(rect.center),  1, 0])
            bullets.append([list(rect.center), -1, 0])
            props["cooldown"] = 120
            asset_manager.get_sound("shoot.wav").play()

    elif name == "aimbot":
        props["cd"] -= 1
        if props["cd"] > 0:
            return

        alive_players = [ p for p in players if p.alive ]

        if not alive_players:
            return

        target = random.choice(alive_players).rect

        dx = target.centerx - rect.centerx
        dy = target.centery - rect.centery
        dist = hypot(dx, dy)

        if not 0 < dist < 500:
            return

        for b in collideblocks:
            if b[0].clipline(target.center, rect.center):
                return

        vx = dx / dist
        vy = dy / dist

        bullets.append([list(rect.center), vx, vy])
        props["cd"] = 70
        asset_manager.get_sound("shoot.wav").play()

    elif name == "falling":
        if props["state"] == "fall":
            if props["cd"] > 0:
                props["cd"] -= 1
            else:
                props["vel_y"] += consts.GRAVITY
                rect.y += props["vel_y"]
                if rect.y > props["pos"] + 1500:
                    props["state"] = "fly"

        elif props["state"] == "fly":
            props["cd"] = 12
            props["vel_y"] = 0
            rect.y = props["pos"]

    elif name == "trampoline":
        for p in players:
            if not p.alive or p.vel_y < 1:
                continue

            p_rect = pg.Rect(
                p.rect.x, p.rect.y + p.vel_y,
                p.rect.width, p.rect.height
            )

            block_hitbox = pg.Rect(
                rect.x, rect.y + (consts.TS * 0.4),
                rect.width, rect.height - (consts.TS * 0.4)
            )

            if p_rect.colliderect(block_hitbox):
                p.vel_y = consts.TRAMPOLINE_VEL
                asset_manager.get_sound("trampoline.wav").play()
                p.rotating = True

    elif name == "checkpoint":
        if props["status"] == "active":
            return

        for p in players:
            if not p.rect.colliderect(rect):
                continue

            asset_manager.get_sound("checkpoint.wav").play()
            props["status"] = "active"
            game.respawn_point = rect.topleft

    elif name == "box":
        props["vel_y"] += consts.GRAVITY
        for col_b in blocks:
            if block == col_b or not col_b[0].colliderect(
                rect.x,
                rect.y + props["vel_y"],
                consts.TS,
                consts.TS
            ):
                continue

            if col_b[2] == "enemy" and props["vel_y"] > 2:
                props["vel_y"] = -6
                asset_manager.get_sound("enemy_hit.wav").play()
                if col_b in blocks:
                    blocks.remove(col_b)

            elif col_b[2] in solid_blocks:
                # if col_b[2] == "box":
                #     block[3]["dx"] == col_b[3]["dx"]
                #     update_block(col_b)
                props["vel_y"] = 0

            elif col_b[2] == "trampoline":
                props["vel_y"] = consts.TRAMPOLINE_VEL

        for player in players:
            if not player.alive or props["vel_y"] < 2:
                continue

            if player.rect.colliderect(
                rect.x,
                rect.y + props["vel_y"],
                consts.TS,
                consts.TS
            ):
                props["vel_y"] = -6
                player.kill()

        rect.y += props["vel_y"]
        rect.x += props["dx"]
        # block[3]["dx"] = 0

    elif name == "flag":
        collision = rect.colliderect(player1.rect)

        if game.players == 2:
            collision &= rect.colliderect(player2.rect)

        if collision:
            asset_manager.get_sound("level_completed.wav").play()
            game.level += 1

            game.stop_player_move = True
            load_level(game.level)

    elif name == "spike":
        for player in players:
            if not player.alive or player.vel_y < 2:
                continue

            if player.velrect().colliderect(
                rect.x,
                rect.y + (rect.height / 2),
                rect.width,
                rect.height / 2
            ):
                player.kill()
                # p.deaths += 1
                # p.explode()
                # game_over(f"P{p.num} jumped into a spike")


def draw_players():
    player1.draw()
    if game.players == 2:
        player2.draw()


def update_players():
    player1.move(left, right)
    player1.update()

    if game.players == 2:
        player2.move(left2, right2)
        player2.update()


def update_lasers():
    for laser in lasers:
        for player in players:
            if player.alive and player.rect.clipline(laser):
                player.kill()


def draw_lasers():
    for laser in lasers:
        pg.draw.line(
            screen,
            "red",
            (laser[0][0]+cam.x, laser[0][1]+cam.y),
            (laser[1][0]+cam.x, laser[1][1]+cam.y),
            5
        )


game.color_selection()
level_selection(screen, game)
load_level(game.level)

should_pause = False
running = True
while running:
    if not vsync:
        consts.clock.tick(consts.FPS)

    # handle input
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:

            if event.key == pg.K_k:
                game.flying = not game.flying

            if event.key == pg.K_r:
                reload = not event.mod & pg.KMOD_LSHIFT
                load_level(game.level, reload)

            if event.key == pg.K_F2:
                util.screenshot()
                should_pause = True

            if event.key in [pg.K_ESCAPE, pg.K_SPACE]:
                should_pause = True

            if event.key == pg.K_F11:
                fullscreen = not fullscreen
                pg.display.toggle_fullscreen()

            # player 1
            if event.key == pg.K_w:
                player1.jump = True
            if event.key == pg.K_a:
                left = True
            if event.key == pg.K_d:
                right = True

            # player 2
            if event.key == pg.K_UP:
                player2.jump = True
            if event.key == pg.K_RIGHT:
                right2 = True
            if event.key == pg.K_LEFT:
                left2 = True

        if event.type == pg.KEYUP:
            # player 1
            if event.key == pg.K_w:
                player1.jump = False
            if event.key == pg.K_a:
                left = False
            if event.key == pg.K_d:
                right = False

            # player 2
            if event.key == pg.K_UP:
                player2.jump = False
            if event.key == pg.K_RIGHT:
                right2 = False
            if event.key == pg.K_LEFT:
                left2 = False

    if should_pause:
        game.stop_player_move = True
        game.load_level_bool = False
        pause()
        if game.load_level_bool:
            level_selection(screen, game)
            if game.level_selected:
                load_level(game.level)
                game.load_level_bool = False
        should_pause = False

    if game.stop_player_move:
        left,  right = False, False
        left2, right2 = False, False
        for p in players:
            p.vel_y = 0
            p.jump = False
            p.knockback = 0
        game.stop_player_move = False

    # update
    update_players()
    update_lasers()
    update_blocks()
    cam.update()
    update_bullets()

    # render
    screen.fill(consts.bg_color)

    draw_bg_lines()
    draw_blocks()
    draw_players()
    draw_bullets()
    draw_lasers()
    draw_stats()

    pg.display.update()


pg.quit()
sys.exit()
