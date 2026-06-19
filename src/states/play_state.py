import pygame as py
from .base_state import BaseState
import config

class PlayState(BaseState):
    def __init__(self, resource_manager, physics, pseudo_3D, Paddle, Ball):
        super().__init__(resource_manager)
        self.physics = physics
        self.pseudo_3D = pseudo_3D
        self.player_paddle = Paddle(config.TABLE_MIDDLE_X, config.PLAYER_SIDE_Y)
        self.ball = Ball()

        self.is_paused = False
        self.target_mouse_x = 0
        self.target_mouse_y = 0
        self.target_z_change = 0


    def enter(self, datos=None): 
        pass

    def exit(self): 
        pass

    def handle_input(self, events : list[py.event.Event]) -> None:
        #reinicio de la acumulacion de la ruedita del mouse
        self.wheel_z_change = 0
        #Eventos discretos (no continuos)
        for event in events:
            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    self.next_state = "MENU"
                elif event.key == py.K_p:
                    self.is_paused = not self.is_paused
            
            elif event.type == py.MOUSEBUTTONDOWN and not self.is_paused:
                if event.button == py.BUTTON_WHEELUP: self.wheel_z_change = config.WHEEL_SENSITIVITY
                if event.button == py.BUTTON_WHEELDOWN: self.wheel_z_change = -config.WHEEL_SENSITIVITY
        
        if self.is_paused: 
            return

        #Inputs continuos (como el mouse)

        #Posicion del mouse para la raqueta en X e Y simulados 3D
        self.target_mouse_x, self.target_mouse_y = py.mouse.get_pos()

        #Altura en Z, mediante teclas
        keys = py.key.get_pressed()
        self.keybord_direction_z = 0
        if keys[py.K_e]: self.keybord_direction_z = 1 #SUBE
        if keys[py.K_SPACE]: self.keybord_direction_z = -1 #BAJA
            
    
    def update(self, dt: float) -> None:
        if self.is_paused:
            return
        
        keyboard_z_delta = self.keybord_direction_z * config.PADDLE_SPEED_Z * dt
        target_z_change = keyboard_z_delta + self.wheel_z_change
        #pasamos las coordenadas de las inputs a la raqueta del jugador
        self.player_paddle.update_pos(self.target_mouse_x, self.target_mouse_y, target_z_change)

        
    
    def render(self, screen: py.Surface) -> None:
        ##PROVISIONAL
        paddle_sx, paddle_sy, paddle_scale = self.pseudo_3D.world_to_screen(
            self.player_paddle.x, self.player_paddle.y, self.player_paddle.z,
            self.player_paddle.width, self.player_paddle.height
        )