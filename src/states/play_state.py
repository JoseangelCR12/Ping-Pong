import pygame as py
from .base_state import BaseState
import config
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..systems.renderer import Renderer
    from ..systems.physics import Physics
    from ..systems.pseudo_3D import Pseudo3D
    from ..entities import *

class PlayState(BaseState):
    def __init__(self, resource_manager, renderer: "Renderer", physics: "Physics", pseudo_3D: "Pseudo3D", Paddle: type["Paddle"], Ball: type["Ball"], Table: type["Table"]):
        super().__init__(resource_manager)
        self.renderer = renderer
        self.physics = physics
        self.pseudo_3D = pseudo_3D
        self.player_paddle = Paddle(0, config.PLAYER_SIDE_Y)
        self.ball = Ball(0, config.PLAYER_SIDE_Y - 20)
        self.table = Table(0, config.NET_Y, 0)

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
                    self.next_state = "MENU"
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
        self.mouse_sx, self.mouse_sy = py.mouse.get_pos()
            
    
    def update(self, dt: float) -> None:
        if self.is_paused:
            return
        #Traducimos la posicion del mouse a el espacio 3D
        target_x, target_y = self.pseudo_3D.mouse_to_world(self.mouse_sx, self.mouse_sy)
        #pasamos las coordenadas traducidas a la raqueta del jugador
        self.player_paddle.update_pos(target_x, target_y, self.target_z_change)

        ###
        self.test_paddle.update_pos(target_x, target_y + 224, self.target_z_change)
        ###

        
    
    def render(self, screen: py.Surface) -> None:
        ##SUPER PROVISIONAL
        table_infleft_sx, table_max_sy, _ = self.pseudo_3D.world_to_screen(
            self.table.x - self.table.half_width, self.table.y - self.table.half_length, self.table.z)
        table_supleft_sx, _, _ = self.pseudo_3D.world_to_screen(
            self.table.x - self.table.half_width, self.table.y + self.table.half_length, self.table.z)
        table_supright_sx, table_min_sy, _ = self.pseudo_3D.world_to_screen(
            self.table.x + self.table.half_width, self.table.y + self.table.half_length, self.table.z)
        table_infright_sx, _, _ = self.pseudo_3D.world_to_screen(
            self.table.x + self.table.half_width, self.table.y - self.table.half_length, self.table.z)
        self.renderer.render_by_scanlines((table_infleft_sx, table_supleft_sx, table_min_sy, table_max_sy, config.WINDOW_WIDTH // 2), self.resource_manager.get_texture("PLAY", "table"))
        self.renderer.render_px((table_infleft_sx, table_supright_sx, table_supleft_sx, table_infright_sx, table_max_sy, table_min_sy))
        ##PPPP

        ########
        testp_sx, testp_sy, testp_scale = self.pseudo_3D.world_to_screen(
            self.test_paddle.x, self.test_paddle.y, self.test_paddle.z
            )
        
        shadow_sx, shadow_sy, _ = self.pseudo_3D.world_to_screen(
            self.test_paddle.x, self.test_paddle.y, self.table.z
            )

        shadow_width, shadow_depth, shadow_opacity = self.pseudo_3D.get_shadow_properties(self.test_paddle.z, testp_scale, self.test_paddle.width, self.test_paddle.thickness)
        self.renderer.render_ellipse((shadow_sx - shadow_width // 2, shadow_sy - shadow_depth // 2, shadow_width, shadow_depth), shadow_opacity, -self.test_paddle.angle)

        ########
        layers = self.resource_manager.get_sprite_stack("PLAY", "paddle", -self.test_paddle.angle)
        self.renderer.render_sprite_stack(layers, testp_sx, testp_sy, testp_scale)

        ##PROVISIONAL
        paddle_sx, paddle_sy, paddle_scale = self.pseudo_3D.world_to_screen(
            self.player_paddle.x, self.player_paddle.y, self.player_paddle.z
            )

        shadow_sx, shadow_sy, _ = self.pseudo_3D.world_to_screen(
            self.player_paddle.x, self.player_paddle.y, self.table.z
            )
        
        shadow_width, shadow_depth, shadow_opacity = self.pseudo_3D.get_shadow_properties(self.player_paddle.z, paddle_scale, self.player_paddle.width, self.player_paddle.thickness)
        self.renderer.render_ellipse((shadow_sx - shadow_width // 2, shadow_sy - shadow_depth // 2, shadow_width, shadow_depth), shadow_opacity, self.player_paddle.angle)

        layers = self.resource_manager.get_sprite_stack("PLAY", "paddle", self.player_paddle.angle)
        self.renderer.render_sprite_stack(layers ,paddle_sx, paddle_sy, paddle_scale)


