import pygame as py
from pygame.event import Event
from .base_state import BaseState
import config
from ..core.settings import data
from ..ui.ui_loader import load_ui
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..systems import *

class WinState(BaseState):
    def __init__(self, resource_manager, audio: "Audio", renderer: "Renderer"):
        super().__init__(resource_manager)
        self.audio = audio
        self.renderer = renderer

        self.state_name = "WIN"


    def enter(self):
        #Cargar elementos de ui: iconos, texto, etc
        self.ui_elements = load_ui(self.state_name, self.resource_manager, self.audio)
        self.icons = self.ui_elements["icons"]
        self.texts = self.ui_elements["texts"]

        self.audio.stop_music()
        self.audio.play_music(self.state_name, "menu_music")
        self.audio.play_sound(self.state_name, "win_sound")

    def exit(self):
        self.audio.stop_music()


    def handle_input(self, events: list[Event]) -> None:
        for event in events:
            if event.type == py.KEYDOWN:
                self.next_change_state = "MENU"

    def update(self, dt):
        pass

    def render(self, screen):
        screen_tuple = (config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2, *config.WINDOW_SIZE)
        self.renderer.render_rectangle(screen_tuple, 50)

        for icon in self.icons.values():
            icon.draw(screen)
        for text in self.texts.values():
            text.draw(screen)