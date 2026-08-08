import pygame as py
from .base_state import BaseState
import config
from ..core.settings import data
from ..ui.ui_loader import load_ui
from typing import TYPE_CHECKING
if TYPE_CHECKING:

    from ..systems import *
    from ..entities import *

class PlayState(BaseState):
    def __init__(self, resource_manager, audio: "Audio", renderer: "Renderer", world_renderer: "WorldRenderer", Physics: type["Physics"], GameRules: type["GameRules"], CPUBrain: type["CPUBrain"], Paddle: type["Paddle"], Ball: type["Ball"], Table: type["Table"], Net: type["Net"]):
        super().__init__(resource_manager)
        self.audio = audio
        self.renderer = renderer
        self.Physics = Physics
        self.game_rules = GameRules()
        self.CPUBrain = CPUBrain
        self.world_renderer = world_renderer
        self.player_paddle = Paddle(0, 0)
        self.ball = Ball(0, config.PLAYER_SIDE_Y - 20)
        self.table = Table(0, config.NET_Y, config.Z_TABLE)
        self.net = Net(0, config.NET_Y, config.Z_TABLE) 

        self.state_name = "PLAY"

        ##
        self.cpu_paddle = Paddle(0, config.Y_MAX)
        ##

        #Delay al empezar
        self.start_delay = 3.0


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
        self.net_texture = self.resource_manager.get_texture(self.state_name, "net")
        self.net_bottom = self.resource_manager.get_texture(self.state_name, "net_bottom")
        self.ball_texture = self.resource_manager.get_texture(self.state_name, "ball")

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

        #Cargamos la ui y guardamos los subdiccionarios de elementos
        self.ui_elements = load_ui(self.state_name, self.resource_manager, self.audio)
        self.texts = self.ui_elements["texts"]

        #Reproducimos la musica
        self.audio.stop_music()
        self.audio.play_music(self.state_name, "in-game_music")
                                      
    def handle_input(self, events : list[py.event.Event]) -> None:
        #reinicio de la acumulacion de la ruedita del mouse
        wheel_z_change = 0
        #Eventos discretos (no continuos)
        for event in events:
            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    self.next_push_state = "PAUSE"

                #A la hora de sacar, usas el espacio para elevar la pelota (toss)
                if event.key == py.K_SPACE:
                    if self.game_rules.current_server == "PLAYER" and self.game_rules.toss_ball():
                        self.ball.vz = 200 #Le damos un impulso hacia arriba a la pelota

                ## PARA TESTEO, RESPAWNEA PELOTA
                if event.key == py.K_g:
                    self.ball.update_pos(0, config.PLAYER_SIDE_Y + 20, config.Z_TABLE + 50)
                    self.ball.vx = 0.0
                    self.ball.vy = 0.0
                    self.ball.vz = 0.0
                    self.game_rules.reset_rally_state()

                ##
            
            elif event.type == py.MOUSEBUTTONDOWN:
                if event.button == py.BUTTON_WHEELUP: wheel_z_change = data.get("wheel_sensitivity", 15)
                if event.button == py.BUTTON_WHEELDOWN: wheel_z_change = -data.get("wheel_sensitivity", 15)
                if event.button == py.BUTTON_RIGHT: self.player_paddle.twiddle = not self.player_paddle.twiddle
        self.target_z_change = wheel_z_change

        #Inputs continuos (como el mouse)

        #Posicion del mouse para la raqueta en X e Y simulados 3D
        self.mouse_x, self.mouse_y = py.mouse.get_pos()
            
    
    def update(self, dt: float) -> None:
        if self.start_delay > 0.0:
            self.start_delay -= dt

            #Detenemos el update
            return
        
        #Actualizamos a la cpu y comprobamos si ha pegado
        cpu_has_hit = self.CPUBrain.calculate_and_move(self.cpu_paddle, self.ball, self.table.get_limits(), dt)
        #Logica pre-saque
        if not self.game_rules.waiting_for_serve:
            #Actualizamos las fisicas
            self.Physics.move_ball(self.ball, dt) #actualizamos la pelota

            hit_paddle =  self.Physics.check_paddle_collision(self.ball, self.player_paddle, dt) #verificamos colision con la raqueta del jugador

                #Verficamos colisiones con otros elementos
            hit_table = self.Physics.check_surface_collision(self.ball, self.table.get_limits())
            if hit_table:
                self.audio.play_sound(self.state_name, "bounce_sound_1")
            hit_floor = self.Physics.check_floor_collision(self.ball)
            if hit_floor:
                self.audio.play_sound(self.state_name, "bounce_sound_2")
            hit_net = self.Physics.check_net_collision(self.ball, self.net.get_limits())
            if hit_net:
                self.audio.play_sound(self.state_name, "hit_net")

            #Ahora verificamos el partido con el modulo de reglas (arbitro)
            result = self.game_rules.evaluate_frame(hit_table, hit_floor, hit_net, self.ball.y)
            
            #Si hubo un golpe del jugador, se empieza a contar el tiempo para tener un treshold para el doble toque en el saque
            if self.game_rules.fault_delay < 1.0:
                self.game_rules.fault_delay -= dt
                
            if hit_paddle:
                if self.game_rules.last_hit_by != "PLAYER":    
                    self.audio.play_sound(self.state_name, "hit_sound")
                    self.game_rules.fault_delay -= dt
                self.game_rules.register_paddle_hit("PLAYER")
        
            ###El modulo de la cpu registra cuando le pega
            if cpu_has_hit:
                self.audio.play_sound(self.state_name, "hit_sound")
                self.game_rules.register_paddle_hit("CPU")
            ###
            
            ##Verificamos el resultado
            if result == "POINT" or self.game_rules.rally_over:
                if self.game_rules.new_rally_delay == 3.0:
                    self.audio.play_sound(self.state_name, "beep")
                self.game_rules.start_next_rally(dt)

            if result == "LET":
                self.game_rules.start_next_rally(dt)
                
            if result == "MATCH_OVER":
                if self.game_rules.winner == "PLAYER":
                    self.next_push_state = "WIN"
                else: 
                    self.next_push_state = "GAMEOVER"

        elif self.game_rules.current_server == "PLAYER" and self.game_rules.is_tossed is False: #Si le toca sacar al jugador
            #El jugador no puede pasar de la mitad antes de sacar
            self.mouse_y = max(self.mouse_y, config.WINDOW_HEIGHT // 2)
            #La pelota se mantiene delante de la raqueta
            self.ball.x = self.player_paddle.x
            self.ball.y = self.player_paddle.y + 40
            self.ball.z = self.player_paddle.z
            self.ball.vx, self.ball.vy, self.ball.vz = 0, 0, 0

        elif self.game_rules.current_server == "CPU": #si le toca sacar al cpu
            if self.CPUBrain.serve(self.cpu_paddle, self.ball, self.game_rules.toss_ball, dt):
                self.audio.play_sound(self.state_name, "hit_sound")
                self.game_rules.register_paddle_hit("CPU") #le decimos a las reglas que hubo contacto

        #Enviamos la informacion del mouse a la raqueta, la cual aplica el clamp y guarda la posicion tridimensional al traducir coordenadas del mouse
        self.player_paddle.mouse_to_world(self.mouse_x, self.mouse_y, self.target_z_change, dt)



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
            1, 16, False, surface=self.table_edge, has_shadow=False
            )
        
        #La malla, la cual esta dividida en dos sprites, el sprite de lo que esta por encima de la mesa, y el sprite de los soportes que van por debajo
        self.world_renderer.add_xz_element(
            self.net.x, self.net.y, self.net.z + 14, 
            self.state_name, "net", self.table.z,
            self.table.y - self.table.half_length,
            2, 28, False, surface=self.net_texture, has_shadow=False
            )
        
        self.world_renderer.add_xz_element(
            self.net.x, self.net.y, self.net.z - 2, 
            self.state_name, "net_bottom", self.table.z,
            self.table.y - self.table.half_length,
            2, 5, False, surface=self.net_bottom, has_shadow=False
            )
        
        #Las raquetas que se actualizan constantemente
        self.world_renderer.add_xz_element(
            self.cpu_paddle.x, self.cpu_paddle.y, self.cpu_paddle.z,
            self.state_name, "paddle", self.table.z, self.table.y - self.table.half_length, 
            self.cpu_paddle.thickness, self.cpu_paddle.height, True, -self.cpu_paddle.angle, 
            None, self.cpu_paddle.width
            )

        self.world_renderer.add_xz_element(
            self.player_paddle.x, self.player_paddle.y, self.player_paddle.z,
            self.state_name, "paddle", self.table.z, self.table.y - self.table.half_length, 
            self.player_paddle.thickness, self.player_paddle.height, True, self.player_paddle.angle, 
            None, self.player_paddle.width
            )
        
        #La pelota que se actualiza constantemente
        self.world_renderer.add_xz_element(
            self.ball.x, self.ball.y, self.ball.z,
            self.state_name, "ball", self.table.z, self.table.y - self.table.half_length,
            self.ball.radius * 3, self.ball.radius, False, 0,
            None, self.ball.radius * 3
        )

        #Renderizamos el mundo pseudo3D
        self.world_renderer.render_world()


        #Ahora elementos de UI
        for text in self.texts.values():
            text.draw(screen)
        #El color de las letras pequeñas varia en funcion del mapa en el que estemos
        text_color = "white"
        text_color_1 = text_color
        if data["theme"] == "purple": 
            text_color = "yellow"
            text_color_1 = (100, 100, 120)

        #Mostramos el puntaje
        font = self.resource_manager.get_font(self.state_name, "main_font", 24)
        player_score = font.render(f"{self.game_rules.player_score}", True, text_color_1)
        cpu_score = font.render(f"{self.game_rules.cpu_score}", True, text_color_1)
        self.renderer.render_sprite(player_score, (config.WINDOW_WIDTH // 2) + 290, (config.WINDOW_HEIGHT // 2) - 30)
        self.renderer.render_sprite(cpu_score, (config.WINDOW_WIDTH // 2) - 280, (config.WINDOW_HEIGHT // 2) - 30)

        #Mostramos los segundos al iniciar
        screen_tuple1 = (config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2 - 40)
        screen_tuple2 = (config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2 + 40)
        if self.start_delay > 0:
            countdown_text = f"¡¡Preparado!! {int(self.start_delay) + 1}"

            server_text = None
            if self.game_rules.current_server == "PLAYER":
                server_text = "¡Tú estás al saque!"
            elif self.game_rules.current_server == "CPU":
                server_text = "¡CPU al saque!"

            font = self.resource_manager.get_font(self.state_name, "main_font", 45)
            text1_surface = font.render(countdown_text, True, text_color)
            self.renderer.render_sprite(text1_surface, *screen_tuple1)
            if server_text is not None:
                text2_surface = font.render(server_text, True, text_color)
                self.renderer.render_sprite(text2_surface, *screen_tuple2)

        #instruccion a la hora de sacar
        if self.game_rules.current_server == "PLAYER" and self.game_rules.is_service:
            font = self.resource_manager.get_font(self.state_name, "main_font", 16)
            guide_text = font.render("Dale a 'Espacio' para elevar la pelota para sacar", True, text_color)
            self.renderer.render_sprite(guide_text, config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT - 24)
