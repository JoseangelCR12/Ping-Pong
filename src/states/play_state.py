import pygame as py
from .base_state import BaseState
import config
from ..core.settings import data
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
        self.player_paddle = Paddle(0, 0)
        self.ball = Ball(0, config.PLAYER_SIDE_Y - 20)
        self.table = Table(0, config.NET_Y, config.Z_TABLE)

        self.state_name = "PLAY"

        ##
        self.test_paddle = Paddle(0, config.Y_MAX)
        ##


    #Metodos que ejecuta el state manager 
    def pause(self):
        #Guardamos la posicion del mouse al entrar al menu de pausa (o a los estados de win/gameover)
        self.playing_mouse = py.mouse.get_pos()
        py.mouse.set_visible(True) #Mouse visible

    def resume(self):
        #enviamos el mouse a la posicion que tenia antes de pausar 
        py.mouse.set_pos(self.playing_mouse)
        py.mouse.set_visible(False)  # Oculta el cursor del mouse

    def enter(self): 
        #cargamos las texturas que no se rotan cada frame
        self.floor_texture = self.resource_manager.get_texture(self.state_name, "floor")
        self.table_texture = self.resource_manager.get_texture(self.state_name, "table")
        self.table_edge = self.resource_manager.get_texture(self.state_name, "table_edge")
        #creamos la surface de la sombra de la mesa a partir del sprite original
        color = (0, 0, 0) #Color negro, la transparecia se le coloca la superficie final escalada con perspectiva
        self.shadow_table = self.table_texture.copy() #Para no modificar el surface original
        self.shadow_table.fill(color, special_flags=py.BLEND_RGB_MULT) #Rellenamos las areas del sprite que estaban coloreadas

        #Iniciamos las variables de inputs del mouse
        self.mouse_x = 0
        self.mouse_y = 0
        self.target_z_change = 0

        #Controlamos el mouse al iniciar el juego
        py.mouse.set_pos(config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT)
        py.event.set_grab(True)  # Captura el mouse para que no salga de la ventana
        py.mouse.set_visible(False)  # Oculta el cursor del mouse

    def handle_input(self, events : list[py.event.Event]) -> None:
        #reinicio de la acumulacion de la ruedita del mouse
        wheel_z_change = 0
        #Eventos discretos (no continuos)
        for event in events:
            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    self.next_push_state = "PAUSE"
            
            elif event.type == py.MOUSEBUTTONDOWN:
                if event.button == py.BUTTON_WHEELUP: wheel_z_change = data.get("wheel_sensitivity", 15)
                if event.button == py.BUTTON_WHEELDOWN: wheel_z_change = -data.get("wheel_sensitivity", 15)
                if event.button == py.BUTTON_RIGHT: self.player_paddle.twiddle, self.test_paddle.twiddle = not self.player_paddle.twiddle, not self.test_paddle.twiddle
        self.target_z_change = wheel_z_change

        #Inputs continuos (como el mouse)

        #Posicion del mouse para la raqueta en X e Y simulados 3D
        self.mouse_x, self.mouse_y = py.mouse.get_pos()
            
    
    def update(self, dt: float) -> None:
        #Enviamos la informacion del mouse a la raqueta, la cual aplica el clamp y guarda la posicion tridimensional al traducir coordenadas del mouse
        self.player_paddle.mouse_to_world(self.mouse_x, self.mouse_y, self.target_z_change, dt)

        ###
        self.test_paddle.update_pos(self.player_paddle.x, config.Y_MAX - self.player_paddle.y , self.player_paddle.z, dt)
        ###
            
    def render(self, screen: py.Surface) -> None:
        
        #Limpiamos la cola de elementos en pantalla cada frame
        self.world_renderer.clear_queue()

        ###Añadimos los elementos a la pantalla

        #El piso
        self.world_renderer.add_xy_element( #HAZ LOS SPRITES MAS ALTOS
            self.table.x, 3 * config.Y_MAX , config.FLOOR_Z, 2700, #Valores arbitrarios para el cuadrado en el espacio 3D
            3 * config.Y_MAX, self.state_name, "floor", self.table.z, self.floor_texture
            )

        #La mesa (junto a su sombra) y su borde
        self.world_renderer.add_xy_element( 
            self.table.x, self.table.y, self.table.z, self.table.half_width, self.table.half_length, 
            self.state_name, "table", config.FLOOR_Z, self.table_texture, self.shadow_table, shadows_on_top=True
            )

        self.world_renderer.add_xz_element(
            self.table.x, config.PLAYER_SIDE_Y, self.table.z - 6, 
            self.state_name, "table_edge", self.table.z, self.table.y - self.table.half_length,
            1, 16, False, surface=self.table_edge
            )
        
        #Las raquetas que se actualizan constantemente
        self.world_renderer.add_xz_element(
            self.test_paddle.x, self.test_paddle.y, self.test_paddle.z,
            self.state_name, "paddle", self.table.z, self.table.y - self.table.half_length, 
            self.test_paddle.thickness, self.test_paddle.height, True, -self.test_paddle.angle, 
            None, self.test_paddle.width
            )

        self.world_renderer.add_xz_element(
            self.player_paddle.x, self.player_paddle.y, self.player_paddle.z,
            self.state_name, "paddle", self.table.z, self.table.y - self.table.half_length, 
            self.player_paddle.thickness, self.player_paddle.height, True, self.player_paddle.angle, 
            None, self.player_paddle.width
            )
        
        #Renderizamos el mundo pseudo3D
        self.world_renderer.render_world()




