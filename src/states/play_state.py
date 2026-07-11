import pygame as py
from .base_state import BaseState
import config
from typing import TYPE_CHECKING
if TYPE_CHECKING:

    from ..systems import *
    from ..entities import *

class PlayState(BaseState):
    def __init__(self, resource_manager, audio: "Audio", renderer: "Renderer", physics: "Physics", world_renderer: "WorldRenderer", Paddle: type["Paddle"], Ball: type["Ball"], Table: type["Table"]):
        super().__init__(resource_manager)
        self.audio = audio
        self.renderer = renderer
        self.physics = physics
        self.world_renderer = world_renderer
        self.player_paddle = Paddle(0, config.PLAYER_SIDE_Y)
        self.ball = Ball(0, config.PLAYER_SIDE_Y - 20)
        self.table = Table(0, config.NET_Y, config.Z_TABLE)

        self.state_name = "PLAY"

        #cargamos texturas estaticas
        self.floor_texture = self.resource_manager.get_texture(self.state_name, "floor")
        self.table_texture = self.resource_manager.get_texture(self.state_name, "table")

        ##
        self.test_paddle = Paddle(0, config.NET_Y)
        ##

        self.is_paused = False
        self.mouse_x = 0
        self.mouse_y = 0
        self.target_z_change = 0

        py.mouse.set_visible(False)  # Oculta el cursor del mouse
        py.event.set_grab(True)  # Captura el mouse para que no salga de la ventana


    def enter(self, datos=None): 
        pass

    def exit(self): 
        pass

    def handle_input(self, events : list[py.event.Event]) -> None:
        #reinicio de la acumulacion de la ruedita del mouse
        wheel_z_change = 0
        #Eventos discretos (no continuos)
        for event in events:
            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    self.next_change_state = "MENU"
                    py.mouse.set_visible(True)
                    py.event.set_grab(False)  # Libera el mouse
                elif event.key == py.K_p:
                    self.is_paused = not self.is_paused
            
            elif event.type == py.MOUSEBUTTONDOWN and not self.is_paused:
                if event.button == py.BUTTON_WHEELUP: wheel_z_change = config.WHEEL_SENSITIVITY
                if event.button == py.BUTTON_WHEELDOWN: wheel_z_change = -config.WHEEL_SENSITIVITY
                if event.button == py.BUTTON_RIGHT: self.player_paddle.twiddle, self.test_paddle.twiddle = not self.player_paddle.twiddle, not self.test_paddle.twiddle
        self.target_z_change = wheel_z_change
        
        if self.is_paused: 
            return

        #Inputs continuos (como el mouse)

        #Posicion del mouse para la raqueta en X e Y simulados 3D
        self.mouse_x, self.mouse_y = py.mouse.get_pos()
            
    
    def update(self, dt: float) -> None:
        if self.is_paused:
            return
        #Enviamos la informacion del mouse a la raqueta, la cual aplica el clamp y guarda la posicion tridimensional al traducir coordenadas del mouse
        self.player_paddle.mouse_to_world(self.mouse_x, self.mouse_y, self.target_z_change, dt)

        ###
        self.test_paddle.mouse_to_world(self.mouse_x, self.mouse_y - config.WINDOW_HEIGHT, self.target_z_change, dt)
        ###
            
    def render(self, screen: py.Surface) -> None:

        self.world_renderer.clear_queue()

        self.world_renderer.add_xy_element(
            self.table.x, 2 * self.table.y , config.Z_FLOOR, int(config.WINDOW_WIDTH * 2.5),
            config.WINDOW_HEIGHT * 2, "floor", self.state_name, self.floor_texture
            )

        self.world_renderer.add_xy_element( 
            self.table.x, self.table.y, self.table.z, self.table.half_width, 
            self.table.half_length, self.state_name, "table", self.table_texture
            )
        
        ######
        self.world_renderer.add_xz_element(
            self.test_paddle.x, self.test_paddle.y, self.test_paddle.z,
            self.table.z, self.test_paddle.width, self.test_paddle.thickness,
            "PLAY", "paddle", None, -self.test_paddle.angle
            )

        ##PROVISIONAL
        self.world_renderer.add_xz_element(
            self.player_paddle.x, self.player_paddle.y, self.player_paddle.z,
            self.table.z, self.player_paddle.width, self.player_paddle.thickness,
            "PLAY", "paddle", None ,self.player_paddle.angle
            )

        self.world_renderer.render_world()




