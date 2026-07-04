import sys
import pygame as py
import config

from .state_manager import StateManager
from ..resources.cache_manager import CacheManager
from ..resources.resource_manager import ResourceManager

from ..systems import *

from ..states import *

from ..entities import *

from .routes import STATE_ROUTES


class Game:
    def __init__(self):
        # Inicialización de Pygame y configuración de la ventana.
        py.init()
        self.screen = py.display.set_mode(config.WINDOW_SIZE, py.SCALED)
        py.display.set_caption(config.TITLE)
        self.clock = py.time.Clock()
        self.running = True

        # Instanciamos sistemas y gestor de caché
        self.physics = Physics()
        self.animator = Animator()
        self.pseudo_3D = Pseudo3D()
        self.audio = Audio()
        self.renderer = Renderer(self.screen)
        self.cache = CacheManager()

        # Guardamos una referencia a las clase de las entidades para que el check_transitions funcione
        self.Paddle = Paddle
        self.Ball = Ball
        self.Table = Table

        #Creamos el manager de recursos
        self.resource_manager = ResourceManager(self.cache)

        self.state_manager = StateManager()

        menu_state = MenuState(self.resource_manager)
        self.state_manager.change_state(menu_state)

    def _check_transitions(self, active_state):
        if active_state and active_state.next_state is not None:
            destination = active_state.next_state
            active_state.next_state = None

            if destination in STATE_ROUTES:
                state_class, dependencies = STATE_ROUTES[destination]
                args = [getattr(self, dep) for dep in dependencies]
                new_state = state_class(*args)

                self.state_manager.change_state(new_state)
            else: print(f"RUTA '{destination}' NO ENCONTRADA")

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
            active_state = self.state_manager.current_state
            
            if active_state:
                active_state.handle_input(events)

                active_state.update(dt)
            
                self._check_transitions(active_state)

                self.screen.fill(config.BG_COLOR)

                active_state.render(self.screen)

            # Actualizar el display.
            py.display.flip()
            
        py.quit()
        sys.exit()