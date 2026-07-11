from entities import config
import math

class CPU:
    def __init__(self, start_x, start_y, start_z):
        #Posición actual de la raqueta de la CPU
        self.x = start_x
        self.y = start_y
        self.z = start_z
        self.angle = 0

        #Historial para que el módulo de físicas también pueda calcular su velocidad
        self.last_x = start_x
        self.last_y = start_y
        self.last_z = start_z

        #Atributos de velocidad que inyectará el módulo de físicas (vx, vy, vz)
        self.vx = 0
        self.vy = 0
        self.vz = 0

        #Dimensiones de la raqueta
        self.width = config.PADDLE_WIDTH
        self.thickness = config.PADDLE_THICKNESS 
        self.height = config.PADDLE_HEIGHT
        
        self.twiddle = False
    
    def get_limits (self):

        """Retorna los límites tridimensionales de la raqueta de la CPU"""

        return (self.x - self.width // 2, self.x + self.width // 2,
                self.y - self.thickness // 2, self.y + self.thickness // 2,
                self.z, self.z + self.height, self.angle, self.twiddle)
    
    def _move_to_target(self, target_x, target_z, dt):
        """Mueve la raqueta suavemente hacia los objetivos X y Z calculados"""
        cpu_speed = config.CPU_MOVE_SPEED * dt

        # Movimiento en X
        if self.x < target_x:
            self.x = min(self.x + cpu_speed, target_x)
        elif self.x > target_x:
            self.x = max(self.x - cpu_speed, target_x)

        # Movimiento en Z
        if self.z < target_z:
            self.z = min(self.z + cpu_speed, target_z)
        elif self.z > target_z:
            self.z = max(self.z - cpu_speed, target_z)
    
    def update (self, ball_pos, ball_speed, dt):
        """Este metodo se encarga de la logica y la decision de la cpu en base a la velocidad de la pelota"""
        #Si la pelota se aleja, regresa al centro para defender
        if ball_speed.y <= 0:
            self._move_to_target(config.DEFAULT_CPU_CENTER_X, config.DEFAULT_CPU_CENTER_Z, dt)
            return

        #Calculo de la magnitud para saber que tan rapido va la pelota
        ball_velocity_magnitude = math.sqrt(ball_speed.x**2 + ball_speed.y**2 + ball_speed.z**2)

        #Si el golpe fue tan debil que no pasara de la malla, la cpu ni reacciona
        if ball_velocity_magnitude < config.MIN_REACTION_SPEED:
            return

        # Distancia en Y que le falta recorrer a la pelota hasta la raqueta de la CPU
        distance_y = self.y - ball_pos.y        

        if ball_speed.y > 0:
            #Tiempo estimado = Distancia / Velocidad (t = d / v)
            time_to_reach = distance_y / ball_speed.y

            #Movimiento rectilíneo uniforme para X (Fricción simplificada de config)
            predicted_x = ball_pos.x + (ball_speed.x * config.FRICTION) * time_to_reach

            #Tiro parabólico para Z: z(t) = z0 + vz*t - 0.5 * g * t^2
            gravity_per_frame = config.GRAVITY / 60.0
            predicted_z = ball_pos.z + (ball_speed.z * time_to_reach) - (0.5 * gravity_per_frame * (time_to_reach ** 2))
        
            #Clampeamos la predicción Z a los límites físicos de la mesa/piso
            predicted_z = max(config.table_z, min(predicted_z, config.MAX_PADDLE_Z))
            
            #Si el cálculo predice que la pelota tocará el piso (Z <= FLOOR) antes de llegar a la CPU 
            #o si se va absurdamente fuera de los límites X de la mesa, la CPU no se molesta en correr
            if predicted_z <= config.FLOOR_Z or predicted_x < (config.table_min_x - 20) or predicted_x > (config.table_max_x + 20):
                #Es un tiro muerto o fuera; se queda quieta o vuelve al centro
                return
            
            #Movimiento al punto predicho
            self._move_to_target(predicted_x, predicted_z, dt)

    
