import pygame as pg
import sys

from . import button, consts, util
from .menu_manager import Menu
from .assets import asset_manager


class ColorSelectionMenu(Menu):
    """Color selection menu for players."""
    
    def __init__(self, screen, game_state):
        super().__init__(screen, game_state)
        
        self.lines = [
            ["red", 200, 300, 450],
            ["green", 200, 410, 450],
            ["blue", 200, 520, 450]
        ]
        
        if self.game_state.game.players == 2:
            self.lines.append(["red",   consts.W-450, 300, consts.W-200])
            self.lines.append(["green", consts.W-450, 410, consts.W-200])
            self.lines.append(["blue",  consts.W-450, 520, consts.W-200])
        
        self.c_b1 = [button.p1_red, button.p1_green, button.p1_blue]
        self.c_b2 = [button.p2_red, button.p2_green, button.p2_blue]
        
        self.confirm_r = button.confirm_c.rect
        self.confirm_s = pg.Surface((self.confirm_r.width, self.confirm_r.height))
    
    def handle_events(self):
        """Handle pygame events."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key in [pg.K_SPACE, pg.K_ESCAPE]:
                    self.running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                if self.confirm_r.collidepoint(pos):
                    self.running = False
    
    def update(self):
        """Update menu logic."""
        consts.clock.tick(consts.FPS)
        pos = pg.mouse.get_pos()
        
        # Handle color button dragging
        if pg.mouse.get_pressed()[0]:
            for bu in self.c_b1:
                if pg.Rect(
                    bu.rect.x-25,
                    bu.rect.y-25,
                    bu.rect.width+50,
                    bu.rect.height+50
                ).collidepoint(pos):
                    bu.rect.centerx = pos[0]
                if bu.rect.left < 200:
                    bu.rect.left = 200
                if bu.rect.right > 450:
                    bu.rect.right = 450
            
            if self.game_state.game.players == 2:
                for bu in self.c_b2:
                    if pg.Rect(
                        bu.rect.x - 20,
                        bu.rect.y - 20,
                        bu.rect.width + 40,
                        bu.rect.height + 40
                    ).collidepoint(pos):
                        bu.rect.centerx = pos[0]
                    
                    if bu.rect.left < consts.W - 450:
                        bu.rect.left = consts.W - 450
                    
                    if bu.rect.right > consts.W - 200:
                        bu.rect.right = consts.W - 200
        
        # Update player colors and images
        for i in range(3):
            if self.c_b1[i].rect.left < 200:
                self.c_b1[i].rect.left = 200
            if self.c_b1[i].rect.right > 450:
                self.c_b1[i].rect.right = 450
            
            if self.game_state.game.players == 2:
                if self.c_b2[i].rect.left < consts.W-450:
                    self.c_b2[i].rect.left = consts.W-450
                if self.c_b2[i].rect.right > consts.W-200:
                    self.c_b2[i].rect.right = consts.W-200
            
            self.game_state.player1.color[i] = self.c_b1[i].rect.centerx - 200
            if self.game_state.game.players == 2:
                self.game_state.player2.color[i] = self.c_b2[i].rect.centerx - (consts.W-450)
        
        # Update player images
        self.game_state.player1.images = []
        for c_img in asset_manager.player_images:
            p_img = util.palette_swap(c_img, c_img.get_at(
                (0, 0)), self.game_state.player1.color).convert()
            p_img.set_colorkey((0, 0, 0))
            self.game_state.player1.images.append(p_img)
        
        if self.game_state.game.players == 2:
            self.game_state.player2.images = []
            for c_img in asset_manager.player_images:
                p_img = util.palette_swap(c_img, c_img.get_at(
                    (0, 0)), self.game_state.player2.color).convert()
                p_img.set_colorkey((0, 0, 0))
                self.game_state.player2.images.append(p_img)
    
    def render(self):
        """Render the color selection menu."""
        pos = pg.mouse.get_pos()
        self.screen.fill((50, 50, 50))
        
        button.colored_b(self.confirm_s, self.confirm_r, [80, 80, 80], pos)
        self.screen.blit(self.confirm_s, self.confirm_r)
        util.draw_text(
            self.screen, True, 30, "Done", "white",
            self.confirm_r.centerx, self.confirm_r.centery
        )
        
        for li in self.lines:
            pg.draw.line(self.screen, li[0], [li[1], li[2]], [
                li[3], li[2]], 7)
        
        for bu1 in self.c_b1:
            bu1.draw(self.screen)
        if self.game_state.game.players == 2:
            for bu2 in self.c_b2:
                bu2.draw(self.screen)
        
        # Draw player previews
        p1_pv_image = pg.transform.scale(self.game_state.player1.images[2], (80, 80))
        p1_pv_rect = p1_pv_image.get_rect()
        p1_pv_rect.center = 350, 120
        
        p2_pv_image = pg.transform.scale(self.game_state.player2.images[2], (80, 80))
        p2_pv_rect = p2_pv_image.get_rect()
        p2_pv_rect.center = consts.W - 350, 120
        
        self.screen.blit((p1_pv_image), p1_pv_rect)
        if self.game_state.game.players == 2:
            self.screen.blit((p2_pv_image), p2_pv_rect)
        
        util.draw_text(
            self.screen, True, 30, str(self.game_state.player1.color),
            "white", p1_pv_rect.centerx, consts.H - 100
        )
        
        if self.game_state.game.players == 2:
            util.draw_text(
                self.screen, True, 30, str(self.game_state.player2.color),
                "white", p2_pv_rect.centerx, consts.H - 100
            )