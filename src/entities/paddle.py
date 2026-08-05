import config

class Paddle:
    def __init__(self, start_x, start_y, start_z=0):
        self.x = start_x
        self.y = start_y
        self.z = start_z
        self.angle = 0

        #última posición para calcular velocidades que el modulo fisica usará
        self.last_x = start_x
        self.last_y = start_y
        self.last_z = start_z

        #velocidades
        self.vx = 0
        self.vy = 0
        self.vz = 0

        #las dimensiones de las raquetas
        self.width = config.PADDLE_WIDTH
        self.thickness = config.PADDLE_THICKNESS 
        self.height = config.PADDLE_HEIGHT
    
        #Flag y delta para rotar 180 grados la raqueta de manera progresiva
        self.twiddle = False
        self.delta_twiddle = 0

    def get_limits(self):
        """Retorna los limites de la raqueta en el frame actual (min_x, max_x, min_y, max_y, min_z, max_z), además de el angulo de rotacion de la raqueta"""
        return (self.x - self.width // 2, self.x + self.width // 2,
                self.y - self.thickness // 2, self.y + self.thickness // 2,
                self.z - self.height // 2, self.z + self.height // 2, self.angle)

            
    def mouse_to_world(self, mouse_sx: int, mouse_sy: int, z_delta: int, dt):
        """
        Traduce las coordenadas 2D del mouse a coordenadas 3D para la raqueta (world_x, world_y)
        Actua como clampeo de la raqueta a la mesa
        """
        #Calculo de la profundidad (world_y)
        world_y = config.NET_Y - (mouse_sy * config.NET_Y // config.WINDOW_HEIGHT)

        #Calculo de world_x
        x_proportion = (config.HALF_TABLE_WIDTH * 1.5) / (config.WINDOW_WIDTH // 2)  # Proporción de 1.5 veces la mitad del ancho de la mesa respecto a la mitad de la pantalla
        world_x = int(mouse_sx - config.WINDOW_WIDTH // 2) * x_proportion

        #calculo de z
        target_z = self.z + z_delta
    
        self.update_pos(world_x, world_y, target_z, dt)

    def update_pos(self, target_x, target_y, target_z, dt):
        """Actualiza la posicion de la raqueta en el espacio 3D, limitando la altura y calculando el angulo de rotacion en X"""
        self._angle_x(target_x)

        #Guardamos lo viejo
        self.last_x = self.x
        self.last_y = self.y
        self.last_z = self.z

        #actualizamos lo nuevo
        self.x = target_x
        self.y = target_y

        #Limite de altura
        self.z = max(config.MIN_PADDLE_Z, min(target_z, config.MAX_PADDLE_Z))

        #calcula su velocidad cada que se mueve
        self._calculate_vel(dt)
    

    def get_restitution(self):
        """Retorna la restitución elástica activa según la cara de la raqueta, junto con la que queda del lado contrario"""
        if not self.twiddle:
            return config.PADDLE_RESTITUTION, config.PADDLE_BACK_RESTITUTION  # Goma cara A, luego B
        return config.PADDLE_BACK_RESTITUTION, config.PADDLE_RESTITUTION # Goma cara B (Revés), luego A

    def _calculate_vel(self, dt):
        #calcula la velocidad de la raqueta en cada frame
        #Como se calcula cada frame, el resultado de la diferencia es la velocidad por frame
        if dt > 0:
            self.vx = (self.x - self.last_x) / dt
            self.vy = (self.y - self.last_y) / dt
            self.vz = (self.z - self.last_z) / dt

    def _angle_x(self, target_x):
        """Calcula el angulo de rotacion de la raqueta en el eje X en funcion de la posicion del mouse"""
        #Limite de angulo
        max_angle = 40
        min_angle = -40
        #Calculamos el angulo en funcion de la posicion del mouse
        angle = target_x * 0.25
        angle = int((angle + 5 / 2) // 5) * 5 #Para que el angulo solo varíe de 5 en 5

        #Incremento progresivo para una transicion suave del twiddle
        if self.twiddle and self.delta_twiddle < 180:
            self.delta_twiddle += 5
        elif not self.twiddle and self.delta_twiddle > 0:
            self.delta_twiddle -= 5

        #Limitamos el angulo
        self.angle = (self.delta_twiddle) + max(min_angle, min(angle, max_angle))