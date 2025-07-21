import pygame as pg
import sys

from . import button, consts, util
from .menu_manager import Menu


class PauseMenu(Menu):
    """Pause menu for the game."""
    
    def __init__(self, screen, game_state):
        super().__init__(screen, game_state)
        
        self.resume_r = button.resume_button.rect
        self.resume_s = pg.Surface((self.resume_r.width, self.resume_r.height))
        
        self.quit_r = button.quit_button.rect
        self.quit_s = pg.Surface((self.quit_r.width, self.quit_r.height))
    
    def handle_events(self):
        """Handle pygame events."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.result = 'quit'
                self.running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    self.result = 'quit'
                    self.running = False
                elif event.key == pg.K_ESCAPE or event.key == pg.K_c:
                    self.result = 'resume'
                    self.running = False
            elif event.type == pg.MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                if self.resume_r.collidepoint(pos):
                    self.result = 'resume'
                    self.running = False
                elif self.quit_r.collidepoint(pos):
                    self.result = 'quit'
                    self.running = False
                elif button.load_lvl_b.rect.collidepoint(pos):
                    self.result = 'load_level'
                    self.running = False
                elif button.color_s_b.rect.collidepoint(pos):
                    self.result = 'color_selection'
                    self.running = False
                elif button.mainm_b.rect.collidepoint(pos):
                    self.result = 'main_menu'
                    self.running = False
    
    def update(self):
        """Update menu logic."""
        consts.clock.tick(consts.FPS)
    
    def render(self):
        """Render the pause menu."""
        pos = pg.mouse.get_pos()
        self.screen.fill((0, 0, 80))  # Standard GUI background color
        
        # draw buttons
        button.load_lvl_b.draw(self.screen)
        button.color_s_b.draw(self.screen)
        button.mainm_b.draw(self.screen)
        
        button.green_button(self.resume_s, self.resume_r, pos)
        self.screen.blit(self.resume_s, self.resume_r)
        
        button.green_button(self.quit_s, self.quit_r, pos)
        self.screen.blit(self.quit_s, self.quit_r)
        
        # draw text
        util.draw_text(self.screen, True, 100, "Paused!",
                       "white", consts.CX, 150)
        util.draw_text(
            self.screen, True, 45, "Resume (C)", "white",
            button.resume_button.rect.centerx,
            button.resume_button.rect.centery
        )
        util.draw_text(
            self.screen, True, 45, "Quit (Q)", "white",
            button.quit_button.rect.centerx, button.quit_button.rect.centery
        )


# Legacy function for backward compatibility
def pause(screen):
    """
    Legacy function - use PauseMenu class instead.
    
    Args:
        screen: pygame screen surface
    
    Returns:
        str: Action taken by user - 'resume', 'main_menu', 'load_level', 'color_selection', or 'quit'
    """
    from .menu_manager import GameState
    game_state = GameState(None)  # No game state needed for legacy function
    menu = PauseMenu(screen, game_state)
    return menu.run()