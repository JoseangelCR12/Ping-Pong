import config

class Ball:
    def __init__(self, start_x, start_y, start_z=0):
        #Datos de posición
        self.x = start_x
        self.y = start_y
        self.z = start_z

        #Datos de velocidad
        self.vx = 0.0
        self.vy = 0.0
        self.vz = 0.0

        #Propiedades físicas pasivas de la pelota
        self.restitution = config.BALL_RESTITUTION

        #las dimensiones de la pelota (la hitbox será un cubo)
        self.radius = config.BALL_RADIUS


    def get_limits(self):

        """Retorna los limites de la pelota en el frame actual (min_x, max_x, min_y, max_y, min_z, max_z)"""

        return (self.x - self.radius, self.x + self.radius,
                self.y - self.radius, self.y + self.radius,
                self.z - self.radius, self.z + self.radius)

    def update_pos(self, target_x, target_y, target_z):
        """Método público para actualizar la posición de renderizado"""
        self.x = target_x
        self.y = target_y
        self.z = target_z