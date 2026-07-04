import config
class Ball:
    def __init__(self, start_x, start_y, start_z=0):
        self.x = start_x
        self.y = start_y
        self.z = start_z

        #última posición para calcular velocidades que el modulo fisica usará
        self.last_x = start_x
        self.last_y = start_y
        self.last_z = start_z

        #velocidades
        self.vx = 0
        self.vy = 0
        self.vz = 0

        #las dimensiones de la pelota (la hitbox será un cubo)
        self.radius = config.BALL_RADIUS

    def get_limits(self):
        """Retorna los limites de la pelota en el frame actual (min_x, max_x, min_y, max_y, min_z, max_z)"""
        return (self.x - self.radius, self.x + self.radius,
                self.y - self.radius, self.y + self.radius,
                self.z - self.radius, self.z + self.radius)

    def calculate_vel(self, dt):
        #calcula la velocidad de la raqueta en cada frame
        if dt > 0:
            self.vx = (self.x - self.last_x)/ dt

    def update_pos(self, target_x, target_y, target_z):
        pass