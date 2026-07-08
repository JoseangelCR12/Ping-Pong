import pygame as py
import config
from .base_state import BaseState
from ..ui.ui_loader import load_ui
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..systems.renderer import Renderer

class MenuState(BaseState):
    #Estado del menú principal del juego
    def __init__(self, resource_manager, renderer: "Renderer"):
        super().__init__(resource_manager)
        self.renderer = renderer

        self.buttons = load_ui("MENU", self.resource_manager)
        self.logo = self.resource_manager.get_texture("MENU", "logo")

    def enter(self, datos=None): 
        pass

    def exit(self): 
        pass

    def handle_input(self, events : list[py.event.Event]) -> None:
        for event in events:
            if self.buttons["play"].handle_input(event):
                self.next_state = "PLAY"
            elif self.buttons["credits"].handle_input(event):
                pass
    
    def update(self, dt: float) -> None:
        mouse_pos = py.mouse.get_pos()
        
        for button in self.buttons.values():
            button.update(mouse_pos)
    
    def render(self, screen: py.Surface) -> None:
        self.renderer.render_sprite(self.logo, config.WINDOW_WIDTH // 2, 80)
        for button in self.buttons.values():
            button.draw(screen)
        