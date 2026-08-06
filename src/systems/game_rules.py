import config

class GameRules:

    def __init__(self, initial_server="PLAYER"):
        self.current_server = initial_server
        self.is_service = True
        self.last_hit_by = initial_server
        self.total_services_done = 0
        self.waiting_for_serve = True
        self.is_tossed = False

        #Banderas de rebotes
        self.server_side_bounced = False
        self.player_side_bounced = False
        self.cpu_side_bounced = False
        self.touched_net = False

        #Estado del set (A 11 puntos con Deuce)
        self.player_score = 0
        self.cpu_score = 0
        self.match_over = False
        self.winner = None

        self.new_rally_delay = 3.0
        self.rally_over = False

        #La cpu tiene un delay antes de sacar
        self.cpu_toss_delay = 2.0

    def toss_ball(self):
        """Metodo que se llama cuando se realiza un saque"""
        if self.waiting_for_serve and not self.is_tossed:
            self.is_tossed = True
            self.waiting_for_serve = False
            return True
        return False

    def evaluate_frame(self, hit_table, hit_floor, hit_net, ball_y):
        """
        Analiza los eventos fisicos del frame actual a traves de booleanos.
        retorna 'CONTINUE', 'POINT' o 'LET' segun corresponda.
        """

        if self.match_over:
            return "MATCH_OVER"

        #Si toca la red en este frame
        if hit_net:
            self.touched_net = True
            return "CONTINUE"

        #Si toca la mesa en este frame
        if hit_table:
            is_opponent_side = ball_y > config.NET_Y

            #Caso de saque
            if self.is_service:
                if self.last_hit_by == self.current_server:
                    #Determina si el primer rebote ocurrio en el lado correcto de la mesa (lado del que sirve)
                    is_server_side = (self.current_server == "PLAYER" and not is_opponent_side) or (self.current_server == "CPU" and  is_opponent_side)

                    #Primer rebote obligatorio en la lado del saque
                    if not self.server_side_bounced:
                        if not is_server_side:
                            return self._award_point("CPU" if self.current_server == "PLAYER" else "PLAYER") 
                        self.server_side_bounced = True
                        return "CONTINUE"
                    
                    #Segundo rebote obligatorio en la lado del receptor
                    if not is_server_side:
                        #Regla del LET
                        if self.touched_net:
                            self.reset_rally_state() #Reinicia el estado del rally para que el saque se repita
                            return "LET"

                        self.is_service = False #Saque valido, inicia el juego normal

                        #Registramos en que lugar se dio el rebote que inicia la partida
                        if is_opponent_side:
                            self.cpu_side_bounced = True
                        else:
                            self.player_side_bounced = True
                        return "CONTINUE"

                    else:
                        #Segundo rebote en el lado del servidor, punto para el receptor
                        return self._award_point("CPU" if self.current_server == "PLAYER" else "PLAYER")
            
            #Juego normal
            elif self.last_hit_by == "PLAYER":
                if not is_opponent_side:
                    return self._award_point("CPU") #El jugador le pega y pica de su mismo lado
                if self.cpu_side_bounced:   
                    return self._award_point("PLAYER") #El jugador le pega y pica en el lado del receptor dos veces
                self.cpu_side_bounced = True
                self.touched_net = False

            elif self.last_hit_by == "CPU":
                if is_opponent_side:
                    return self._award_point("PLAYER") #La cpu le pega y pica de su mismo lado
                if self.player_side_bounced:   
                    return self._award_point("CPU") #La cpu le pega y pica en el lado del receptor dos veces
                self.player_side_bounced = True
                self.touched_net = False

            return "CONTINUE"
        
        #Si pega en el suelo (pelota fuera)
        if hit_floor:
            #Si toco la red justo antes de caer al suelo, es punto para el receptor
            if self.is_service and self.touched_net:
                return self._award_point("CPU" if self.current_server == "PLAYER" else "PLAYER")

            #Fuera de la mesa en el rally activo
            if self.last_hit_by == "PLAYER":
                return self._award_point("PLAYER" if self.cpu_side_bounced else "CPU")
            elif self.last_hit_by == "CPU":
                return self._award_point("CPU" if self.player_side_bounced else "PLAYER")

        return "CONTINUE"

    def _award_point(self, winner_of_point):
        """
        Metodo interno para actualizar el marcador y el estado del set cuando un jugador gana un punto.
        Rota el servidor si es necesario y determina si el set ha terminado.
        """
        #Si se acaba de dar un punto y no ha empezado otro rally, detenemos los nuevos puntos
        if self.rally_over:
            return "CONTINUE"
        
        self.rally_over = True

        if winner_of_point == "PLAYER":
            self.player_score += 1
        elif winner_of_point == "CPU":
            self.cpu_score += 1

        #Verificamos si el set ha terminado
        if (self.player_score >= 11 or self.cpu_score >= 11) and abs(self.player_score - self.cpu_score) >= 2:
            self.match_over = True
            self.winner = "PLAYER" if self.player_score > self.cpu_score else "CPU"
            return "POINT"

        #Rotamos el servidor cada dos puntos
        self.total_services_done += 1
        if self.player_score >= 10 and self.cpu_score >= 10:
            #En caso de Deuce, el servicio rota cada punto
            self.current_server = "CPU" if self.current_server == "PLAYER" else "PLAYER"
        else:
            if self.total_services_done % 2 == 0:
                self.current_server = "CPU" if self.current_server == "PLAYER" else "PLAYER"
        
        return "POINT"
    
    def register_paddle_hit(self, hitter):
        """
        Registra el impacto de una raqueta
        """
        #Verficamos que no se golpee la pelota antes de que rebote durante el rally activo
        if not self.is_service and self.last_hit_by != hitter:
            if hitter == "PLAYER" and not self.player_side_bounced:
                return self._award_point("CPU")
            elif hitter == "CPU" and not self.cpu_side_bounced:
                return self._award_point("PLAYER")


        #Actualizamos el ultimo golper
        self.last_hit_by = hitter
        return "CONTINUE"
    
    def start_next_rally(self, dt):
        """Espera para iniciar el rally"""
        if self.new_rally_delay > 0.0:
            self.new_rally_delay -= dt

            if self.new_rally_delay <= 0.0:
                self.new_rally_delay = 3.0
                self.reset_rally_state()


    def reset_rally_state(self):
        """Limpia las banderas de rebotes para la siguiente jugada"""
        self.is_service = True
        self.last_hit_by = self.current_server
        self.server_side_bounced = False
        self.player_side_bounced = False
        self.cpu_side_bounced = False
        self.touched_net = False
        self.rally_over = False

        self.waiting_for_serve = True
        self.is_tossed = False