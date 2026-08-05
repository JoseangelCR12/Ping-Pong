import pygame as py
import config
from .base_state import BaseState
from ..core import settings
from ..ui.ui_loader import load_ui
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..systems.audio import Audio
    from ..systems.renderer import Renderer

class PauseState(BaseState):
    #Estado del menu de pausa del juego
    def __init__(self, resource_manager, audio: "Audio", renderer: "Renderer"):
        super().__init__(resource_manager)
        self.audio = audio
        self.renderer = renderer

    def enter(self):
        #Cargamos la ui y guardamos los subdiccionarios de elementos
        self.ui_elements = load_ui("PAUSE", self.resource_manager, self.audio)
        self.buttons = self.ui_elements["buttons"]
        self.icons = self.ui_elements["icons"]
        self.sliders = self.ui_elements["sliders"]

        #Sincronizacion de los sliders con los ajustes
        self.sliders["volume_music"].value = settings.data.get("volume_music", 0.7)
        self.sliders["volume_sfx"].value = settings.data.get("volume_sfx", 0.7)
        self.sliders["wheel_sensitivity"].value = settings.data.get("wheel_sensitivity", 15)  

    def exit(self):
        pass

    def handle_input(self, events : list[py.event.Event]) -> None:
        for event in events:
            if event.type == py.KEYDOWN:
               if event.key == py.K_ESCAPE:
                   self.pop_request = True
                   
            elif self.buttons["menu"].handle_input(event):
                self.next_change_state = "MENU"
                self.audio.stop_music()

            elif self.buttons["restart"].handle_input(event):
                self.next_change_state = "PLAY"
                self.audio.stop_music()
            
            elif self.sliders["volume_music"].handle_input(event):
                #modificamos el volumen de la musica, guardamos en memoria y llamamos al gestor de audio
                new_volume = self.sliders["volume_music"].value
                settings.set_music_volume(new_volume)
                settings.save_to_file()
                self.audio.update_music_volume()
            
            elif self.sliders["volume_sfx"].handle_input(event):
                #modificamos el volumen de los sfx y guardamos en memoria
                new_volume = self.sliders["volume_sfx"].value
                settings.set_sfx_volume(new_volume)
                settings.save_to_file()

            elif self.sliders["wheel_sensitivity"].handle_input(event):
                #modificamos la sensibilidad de la ruedita del mouse y guardamos en memoria
                new_sensitivity = self.sliders["wheel_sensitivity"].value
                settings.set_wheel_sensitivity(new_sensitivity)
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