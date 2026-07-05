import config

class Paddle:
    def __init__(self, start_x, start_y, start_z=config.PADDLE_HEIGHT // 2):
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
    
        #Flag para rotar 180 grados la raqueta
        self.twiddle = False

    def get_limits(self):
        """Retorna los limites de la raqueta en el frame actual (min_x, max_x, min_y, max_y, min_z, max_z), además de el angulo de rotacion de la raqueta"""
        return (self.x - self.width // 2, self.x + self.width // 2,
                self.y - self.thickness // 2, self.y + self.thickness // 2,
                self.z - self.height // 2, self.z + self.height // 2, self.angle)

    def calculate_vel(self, dt):
        #calcula la velocidad de la raqueta en cada frame
        if dt > 0:
            self.vx = (self.x - self.last_x)/ dt

    def update_pos(self, target_x, target_y, z_delta):
        """Actualiza la posicion de la raqueta en el espacio 3D, limitando la altura y calculando el angulo de rotacion en X"""
        self._angle_x(target_x)
        self.x = target_x
        self.y = target_y
        #Limite de altura
        self.z = max(config.MIN_PADDLE_Z, min(self.z + z_delta, config.MAX_PADDLE_Z))
    
    def _angle_x(self, target_x):
        """Calcula el angulo de rotacion de la raqueta en el eje X en funcion de la posicion del mouse"""
        #Limite de angulo
        max_angle = 40
        min_angle = -40
        #Calculamos el angulo en funcion de la posicion del mouse
        angle = target_x * 0.25
        #Limitamos el angulo
        self.angle = (self.twiddle * 180) + max(min_angle, min(angle, max_angle))