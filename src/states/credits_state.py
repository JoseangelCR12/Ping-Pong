import pygame as py
from .base_state import BaseState
from ..ui.ui_loader import load_ui
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..systems.audio import Audio
    from ..systems.renderer import Renderer

class CreditsState(BaseState):
    #Estado del menú principal del juego
    def __init__(self, resource_manager, audio: "Audio", renderer: "Renderer"):
        super().__init__(resource_manager)
        self.audio = audio
        self.renderer = renderer

        self.state_name = "CREDITS"

    def enter(self): 
        py.event.set_grab(False)  # Deja mover el mouse libremente fuera de la ventana
        py.mouse.set_visible(True) # Mouse visible

        #Cargamos la ui y guardamos los subdiccionarios de elementos
        self.ui_elements = load_ui(self.state_name, self.resource_manager, self.audio)
        self.icons = self.ui_elements["icons"]
        self.texts = self.ui_elements["texts"]

    def handle_input(self, events : list[py.event.Event]) -> None:
        for event in events:
            if event.type == py.KEYDOWN:
                self.next_change_state = "MENU"

    def update(self, dt: float) -> None:
        pass
    
    def render(self, screen: py.Surface) -> None:
        #Dibujamos el fondo y los elementos de la ui
        for icon in self.icons.values():
            icon.draw(screen)
        for text in self.texts.values():
            text.draw(screen)
        
        
