import pygame as py
from .base_state import BaseState
from ..ui.ui_loader import load_ui

class MenuState(BaseState):
    #Estado del menú principal del juego
    def __init__(self, resource_manager):
        super().__init__(resource_manager)

        self.buttons = load_ui("MENU", self.resource_manager)

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
        for button in self.buttons.values():
            button.draw(screen)
        