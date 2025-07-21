"""
Menu Manager System

This module provides a base Menu class and MenuManager for handling
all game menus in a class-based architecture.
"""

import pygame as pg
from abc import ABC, abstractmethod


class Menu(ABC):
    """Base class for all menus."""
    
    def __init__(self, screen, game_state):
        """
        Initialize the menu.
        
        Args:
            screen: pygame screen surface
            game_state: shared game state object
        """
        self.screen = screen
        self.game_state = game_state
        self.running = True
        self.result = None
    
    @abstractmethod
    def handle_events(self):
        """Handle pygame events for this menu."""
        pass
    
    @abstractmethod
    def update(self):
        """Update menu logic."""
        pass
    
    @abstractmethod
    def render(self):
        """Render the menu to screen."""
        pass
    
    def run(self):
        """Main menu loop."""
        self.running = True
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            pg.display.update()
        return self.result


class MenuManager:
    """Manages transitions between different menus."""
    
    def __init__(self, screen, game_state):
        """
        Initialize the menu manager.
        
        Args:
            screen: pygame screen surface
            game_state: shared game state object
        """
        self.screen = screen
        self.game_state = game_state
        self.current_menu = None
        self.menu_stack = []
    
    def push_menu(self, menu_class, *args, **kwargs):
        """
        Push a new menu onto the stack and make it current.
        
        Args:
            menu_class: Class of menu to create
            *args, **kwargs: Arguments to pass to menu constructor
        """
        if self.current_menu:
            self.menu_stack.append(self.current_menu)
        
        self.current_menu = menu_class(self.screen, self.game_state, *args, **kwargs)
    
    def pop_menu(self):
        """Pop the current menu and return to previous one."""
        if self.menu_stack:
            self.current_menu = self.menu_stack.pop()
            return True
        return False
    
    def set_menu(self, menu_class, *args, **kwargs):
        """
        Set a new menu, clearing the stack.
        
        Args:
            menu_class: Class of menu to create
            *args, **kwargs: Arguments to pass to menu constructor
        """
        self.menu_stack.clear()
        self.current_menu = menu_class(self.screen, self.game_state, *args, **kwargs)
    
    def run_current_menu(self):
        """Run the current menu and return its result."""
        if self.current_menu:
            return self.current_menu.run()
        return None


class GameState:
    """Shared game state accessible to all menus."""
    
    def __init__(self, game, players=None, player1=None, player2=None, load_level_func=None):
        """
        Initialize game state.
        
        Args:
            game: Main Game object
            players: List of player objects
            player1: Player 1 object
            player2: Player 2 object
            load_level_func: Function to load levels
        """
        self.game = game
        self.players = players or []
        self.player1 = player1
        self.player2 = player2
        self.load_level_func = load_level_func