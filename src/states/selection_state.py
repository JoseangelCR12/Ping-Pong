import pygame as py
import config
from .base_state import BaseState
from ..core import settings
from ..ui.ui_loader import load_ui
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..systems.audio import Audio
    from ..systems.renderer import Renderer

class SelectionState(BaseState):
    #Estado del menu de pausa del juego
    def __init__(self, resource_manager, audio: "Audio", renderer: "Renderer"):
        super().__init__(resource_manager)
        self.audio = audio
        self.renderer = renderer

    def enter(self):
        #Cargamos la ui y guardamos los subdiccionarios de elementos
        self.ui_elements = load_ui("SELECTION", self.resource_manager, self.audio)
        self.buttons = self.ui_elements["buttons"]
        self.icons = self.ui_elements["icons"]
        self.sliders = self.ui_elements["sliders"]
        self.texts = self.ui_elements["texts"]

        #Sincronizacion de los sliders con los ajustes
        self.sliders["cpu_level"].value = settings.data.get("cpu_level", 2)
        
    def exit(self):
        pass

    def handle_input(self, events : list[py.event.Event]) -> None:
        for event in events:
            if event.type == py.KEYDOWN:
               if event.key == py.K_ESCAPE:
                   self.pop_request = True
                   
            elif self.buttons["play"].handle_input(event) and settings.data.get("cpu_level", 2) > 0:
                self.next_change_state = "PLAY"

            elif self.sliders["cpu_level"].handle_input(event):
                #modificamos la sensibilidad de la ruedita del mouse y guardamos en memoria
                new_cpu = self.sliders["cpu_level"].value
                settings.set_cpu_level(new_cpu)
                settings.save_to_file()
                
    def update(self, dt: float) -> None:
        mouse_pos = py.mouse.get_pos()
        
        for button in self.buttons.values():
            button.update(mouse_pos)
        for slider in self.sliders.values():
            slider.update(mouse_pos)
    
    def render(self, screen: py.Surface) -> None:
        #Dibujamos el velo oscuro de la pantalla
        screen_tuple = (config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2, *config.WINDOW_SIZE)
        self.renderer.render_rectangle(screen_tuple, 50)

        for icon in self.icons.values():
            icon.draw(screen)
        for button in self.buttons.values():
            button.draw(screen)
        for slider in self.sliders.values():
            slider.draw(screen)

        level_index = settings.data.get("cpu_level", 2)
        text = self.texts[f"{level_index}"]
        text.draw(screen)
        

        