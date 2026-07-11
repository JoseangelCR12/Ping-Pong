import pygame as py
import config
from .base_state import BaseState
from ..core import settings
from ..ui.ui_loader import load_ui
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..systems.audio import Audio
    from ..systems.renderer import Renderer

class OptionsState(BaseState):
    #Estado del menu de opciones del juego
    def __init__(self, resource_manager, audio: "Audio", renderer: "Renderer"):
        super().__init__(resource_manager)
        self.audio = audio
        self.renderer = renderer

        #
        self.audio.play_music("OPTIONS", "dopodime")
        #

    def enter(self):
        #Cargamos la ui y guardamos los subdiccionarios de elementos
        self.ui_elements = load_ui("OPTIONS", self.resource_manager)
        self.buttons = self.ui_elements["buttons"]
        self.icons = self.ui_elements["icons"]
        self.sliders = self.ui_elements["sliders"]

        #Sincronizacion de los sliders con los ajustes
        self.sliders["volume_music"].value = settings.data.get("volume_music", 0.7)
        self.sliders["volume_sfx"].value = settings.data.get("volume_sfx", 0.7)

        #listas para ciclar las opciones al presionar los botones
        self.themes = ["classic", "udo"]
        self.cameras = ["standard", "fisheye"]

    def exit(self):
        pass

    def handle_input(self, events : list[py.event.Event]) -> None:
        for event in events:
            if event.type == py.KEYDOWN:
               if event.key == py.K_ESCAPE:
                   self.pop_request = True

            elif self.buttons["change_theme"].handle_input(event):
                #Buscamos el tema siguiente
                current_idx = self.themes.index(settings.data["theme"])
                next_idx = (current_idx + 1) % len(self.themes)
                new_theme = self.themes[next_idx]
                #Modificamos el tema, guardamos en memoria el ajuste y vaciamos la cache del tema anterior
                settings.set_theme(new_theme)
                settings.save_to_file()
                self.resource_manager.cache.clear_all()

                #Forzamos a la UI a recargarse
                self.ui_elements = load_ui("OPTIONS", self.resource_manager)

            elif self.buttons["change_camera"].handle_input(event):
                #Buscamos el siguiente modo de camara
                current_idx = self.cameras.index(settings.data["camera_mode"])
                next_idx = (current_idx + 1) % len(self.cameras)
                new_camera = self.cameras[next_idx]
                #Modificamos el tema, guardamos en memoria el ajuste y vaciamos la cache de la vista anterior
                settings.set_camera_preset(new_camera)
                settings.save_to_file()
                self.resource_manager.cache.clear_all()
            
            elif self.sliders["volume_music"].handle_input(event):
                #modificamos el volumen de la musica, guardamos en memoria y llamamos al gestor de audio
                new_volume = self.sliders["volume_music"].value
                settings.set_music_volume(new_volume)
                settings.save_to_file()
                self.audio.update_music_volume()
            
            elif self.sliders["volume_sfx"].handle_input(event):
                #modificamos el volumen de los sfx, guardamos en memoria y llamamos al gestor de audio
                new_volume = self.sliders["volume_sfx"].value
                settings.set_sfx_volume(new_volume)
                settings.save_to_file()

    
    def update(self, dt: float) -> None:
        mouse_pos = py.mouse.get_pos()
        
        for button in self.buttons.values():
            button.update(mouse_pos)
        for slider in self.sliders.values():
            slider.update(mouse_pos)
    
    def render(self, screen: py.Surface) -> None:
        screen_tuple = (config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2, *config.WINDOW_SIZE)
        self.renderer.render_rectangle(screen_tuple, 100)

        for icon in self.icons.values():
            icon.draw(screen)
        for button in self.buttons.values():
            button.draw(screen)
        for slider in self.sliders.values():
            slider.draw(screen)
        