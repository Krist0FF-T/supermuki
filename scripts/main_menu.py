import pygame as pg
from . import button, consts, util
from .menu_manager import Menu


class MainMenu(Menu):
    """Main menu for selecting number of players."""
    
    def __init__(self, screen, game_state):
        super().__init__(screen, game_state)
        self.option = 0
        self.text1 = 'Super Muki'
        self.version = '1.5'
        
        self.b1_r = pg.Rect(100, consts.CY, 400, 200)
        self.b1_s = pg.Surface((self.b1_r.width, self.b1_r.height))
        
        self.b2_r = pg.Rect(consts.W-500, consts.CY, 400, 200)
        self.b2_s = pg.Surface((self.b1_r.width, self.b1_r.height))
    
    def handle_events(self):
        """Handle pygame events."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.result = 0
                self.running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.result = 0
                    self.running = False
                elif event.key == pg.K_1:
                    self.option = 1
                    self.result = 1
                    self.running = False
                elif event.key == pg.K_2:
                    self.option = 2
                    self.result = 2
                    self.running = False
            elif event.type == pg.MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                if self.b1_r.collidepoint(pos):
                    self.option = 1
                    self.result = 1
                    self.running = False
                elif self.b2_r.collidepoint(pos):
                    self.option = 2
                    self.result = 2
                    self.running = False
    
    def update(self):
        """Update menu logic."""
        consts.clock.tick(60)
    
    def render(self):
        """Render the menu."""
        pos = pg.mouse.get_pos()
        self.screen.fill((0, 0, 80))
        
        button.green_button(self.b1_s, self.b1_r, pos)
        button.green_button(self.b2_s, self.b2_r, pos)
        
        self.screen.blit(self.b1_s, self.b1_r)
        self.screen.blit(self.b2_s, self.b2_r)
        
        util.draw_text(
            self.screen, True, 60, '1 Player',
            "white", self.b1_r.centerx, self.b1_r.centery
        )
        
        util.draw_text(
            self.screen, True, 60, '2 Player',
            "white", self.b2_r.centerx, self.b2_r.centery
        )
        
        util.draw_text(
            self.screen, True, 100, self.text1, "white",
            self.screen.get_width() // 2, 150
        )
        
        util.draw_text(
            self.screen, False, 30, f'version: {self.version}',
            "white", 30, consts.H-60
        )


# Legacy function for backward compatibility
def main_menu(surface, game):
    """Legacy function - use MainMenu class instead."""
    from .menu_manager import GameState
    game_state = GameState(game)
    menu = MainMenu(surface, game_state)
    result = menu.run()
    if result:
        game.players = result
