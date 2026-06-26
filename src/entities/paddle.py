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

        #las dimensiones de las raquetas en px, basadas en el sprite, para las hitboxes
        self.width = 30
        self.height = 37
        self.depth = 5

    def calculate_vel(self, dt):
        #calcula la velocidad de la raqueta en cada frame
        if dt > 0:
            self.vx = (self.x - self.last_x)/ dt

    def update_pos(self, target_x, target_y, z_delta):
        #Limites en X e Y
        self.x = max(config.MIN_X + self.width, min(target_x, config.MAX_X))
        self.y = max(config.NET_Y, min(target_y, config.PLAYER_SIDE_Y))
        #Limite de altura
        self.z = max(0, min(self.z + z_delta, config.MAX_Z))
    