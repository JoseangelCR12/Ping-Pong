import pygame as py
from .base_state import BaseState
from ..ui.ui_loader import load_ui
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..systems.audio import Audio

class MenuState(BaseState):
    #Estado del menú principal del juego
    def __init__(self, resource_manager, audio: "Audio"):
        super().__init__(resource_manager)
        self.audio = audio

    def resume(self):
        #Recargamos la ui al venir del menu de opciones
        self.enter()

    def enter(self): 
        py.event.set_grab(False)  # Deja mover el mouse libremente fuera de la ventana
        py.mouse.set_visible(True) # Mouse visible

        #Cargamos la ui y guardamos los subdiccionarios de elementos
        self.ui_elements = load_ui("MENU", self.resource_manager)
        self.buttons = self.ui_elements["buttons"]
        self.icons = self.ui_elements["icons"]

    def handle_input(self, events : list[py.event.Event]) -> None:
        for event in events:
            if self.buttons["play"].handle_input(event):
                self.next_push_state = "SELECTION"
            elif self.buttons["options"].handle_input(event):
                self.next_push_state = "OPTIONS"
            elif self.buttons["credits"].handle_input(event):
                pass
    
    def update(self, dt: float) -> None:
        mouse_pos = py.mouse.get_pos()
        
        for button in self.buttons.values():
            button.update(mouse_pos)
    
    def render(self, screen: py.Surface) -> None:
        for icon in self.icons.values():
            icon.draw(screen)
        for button in self.buttons.values():
            button.draw(screen)
        