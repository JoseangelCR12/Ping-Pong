import sys
import pygame as py
import config

from .state_manager import StateManager
from ..resources.cache_manager import CacheManager
from ..resources.resource_manager import ResourceManager

from .settings import load_from_file
from .routes import STATE_ROUTES

from ..systems import *

from ..states import *

from ..entities import *


class Game:
    def __init__(self):
        # Inicialización de Pygame y configuración de la ventana.
        py.init()
        self.screen = py.display.set_mode(config.WINDOW_SIZE, py.SCALED)
        py.display.set_caption(config.TITLE)
        self.clock = py.time.Clock()
        self.running = True

        #Cargamos datos de guardado de ajustes
        load_from_file()

        # Instanciamos sistemas, gestor de caché y el gestor de recursos
        self.physics = Physics()
        self.renderer = Renderer(self.screen)
        self.cache = CacheManager()

        self.resource_manager = ResourceManager(self.cache)
        self.audio = Audio(self.resource_manager)

        self.world_renderer = WorldRenderer(self.resource_manager, self.renderer)

        # Guardamos una referencia a las clase de las entidades para que el check_transitions las inyecte
        self.Paddle = Paddle
        self.Ball = Ball
        self.Table = Table
        self.Net = Net

        # Instanciamos el gestor de estados e iniciamos el menú
        self.state_manager = StateManager(states_factory=self.states_factory)

        #iniciamos el menu
        menu_state = MenuState(self.resource_manager, self.audio)
        self.state_manager.change_state(menu_state)

    def states_factory(self, destination: str):
        #Fabrica de estados: construye e inyecta dependencias
        if destination in STATE_ROUTES:
            state_class, dependencies = STATE_ROUTES[destination]
            args = [getattr(self, dep) for dep in dependencies]
            return state_class(*args) 
        print(f"RUTA '{destination}' NO ENCONTRADA")
        return None

    def run(self):
        fps_timer, frames = 0 , 0
        """Bucle principal del juego."""
        while self.running:

            dt = self.clock.tick(config.FPS) / 1000  # Tiempo en segundos desde el último frame.
            if dt > 0.1:  # Limitar el delta time para evitar saltos grandes.
                dt = 0.1

            frames += 1
            fps_timer += dt
            if fps_timer >= 1:
                print(f"FPS={self.clock.get_fps():.1f} frames={frames} frame_ms={fps_timer/frames:.2f}")
                fps_timer = 0
                frames = 0

            # Manejo de eventos globales, como cerrar la ventana.
            events = py.event.get()
            for event in events:
                if event.type == py.QUIT:
                    self.running = False

            # Delegar eventos, actualización y renderizado al estado activo.
            self.state_manager.handle_input(events)

            self.state_manager.update(dt)

            self.state_manager.render(self.screen)

            # Actualizar el display.
            py.display.flip()
            
        py.quit()
        sys.exit()