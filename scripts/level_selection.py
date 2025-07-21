import sys
import pygame as pg
from . import consts, util, button
from .menu_manager import Menu


class LevelSelectionMenu(Menu):
    """Level selection menu."""
    
    def __init__(self, screen, game_state):
        super().__init__(screen, game_state)
        
        self.button_quit_r = pg.Rect(50, 50, 160, 90)
        self.button_quit_s = pg.Surface((self.button_quit_r.width, self.button_quit_r.height))
        
        self.lb_width = 120
        self.cd = 10  # 10 frame countdown after mouse key press
        
        self.sr_r = pg.Rect(consts.W-50-250, 50, 250, 90)
        self.sr_s = pg.Surface((self.sr_r.width, self.sr_r.height))
        
        self.b_rows = 2
        self.b_cols = 5
        
        self.result = {'level_selected': False, 'level': 1, 'level_to_load': "1"}
    
    def handle_events(self):
        """Handle pygame events."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                if self.button_quit_r.collidepoint(pos):
                    self.result['level_selected'] = False
                    self.running = False
    
    def update(self):
        """Update menu logic."""
        consts.clock.tick(60)
        pos = pg.mouse.get_pos()
        
        if self.cd > 0:
            self.cd -= 1
        
        # Check level button clicks
        for i in range(self.b_cols):
            for y in range(self.b_rows):
                num = i + (y * self.b_cols) + 1
                option_r = pg.Rect(
                    (140 * i) + 300,
                    (140 * y) + 280,
                    self.lb_width, self.lb_width
                )
                
                if option_r.collidepoint(pos):
                    if self.cd <= 0 and pg.mouse.get_pressed()[0]:
                        self.result['level_to_load'] = f"{num}"
                        self.result['level'] = num
                        self.result['level_selected'] = True
                        self.running = False
    
    def render(self):
        """Render the level selection menu."""
        pos = pg.mouse.get_pos()
        self.screen.fill(self.game_state.game.gui_rgb)
        
        button.green_button(self.button_quit_s, self.button_quit_r, pos)
        self.screen.blit(self.button_quit_s, self.button_quit_r)
        util.draw_text(
            self.screen, True, 40, "Back", "white",
            self.button_quit_r.centerx, self.button_quit_r.centery
        )
        
        button.green_button(self.sr_s, self.sr_r, pos)
        self.screen.blit(self.sr_s, self.sr_r)
        
        for i in range(self.b_cols):
            for y in range(self.b_rows):
                num = i + (y * self.b_cols) + 1
                option_r = pg.Rect(
                    (140 * i) + 300,
                    (140 * y) + 280,
                    self.lb_width, self.lb_width
                )
                option_s = pg.Surface((
                    option_r.width, option_r.height
                ))
                
                option_s.fill(consts.GREEN)
                if option_r.collidepoint(pos):
                    option_s.fill((120, 255, 120))
                    if self.cd <= 0 and pg.mouse.get_pressed()[0]:
                        option_s.fill((50, 50, 50))
                
                self.screen.blit((option_s), option_r)
                util.draw_text(self.screen, True, 50, str(num), "white",
                               option_r.centerx, option_r.centery)
        
        util.draw_text(
            self.screen, True, 60,
            "Level Selection",
            consts.WHITE, consts.CX, 90
        )


# Legacy function for backward compatibility
def level_selection(surface, g):
    """Legacy function - use LevelSelectionMenu class instead."""
    from .menu_manager import GameState
    game_state = GameState(g)
    menu = LevelSelectionMenu(surface, game_state)
    result = menu.run()
    
    if result:
        g.level_selected = result['level_selected']
        g.level = result['level']
        g.level_to_load = result['level_to_load']
