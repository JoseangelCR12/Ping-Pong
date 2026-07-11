import config
from systems.physics import Physics

class Ball:
    def __init__(self, start_x, start_y, start_z=0.0, vx = 0.0, vy = 0.0, vz = 0.0):

        #Instanciamos el componente de fisicas
        self.physics = Physics(x = start_x, y = start_y, z = start_z, vx = vx, vy = vy, vz = vz)

        #posiciones que usara el renderizado/dibujo del juego
        self.x = self.physics.position.x
        self.y = self.physics.position.y
        self.z = self.physics.position.z

        #las dimensiones de la pelota (la hitbox será un cubo)
        self.radius = config.BALL_RADIUS

    def get_limits(self):

        """Retorna los limites de la pelota en el frame actual (min_x, max_x, min_y, max_y, min_z, max_z)"""

        return (self.x - self.radius, self.x + self.radius,
                self.y - self.radius, self.y + self.radius,
                self.z - self.radius, self.z + self.radius)

    def update(self, table, net, paddle):

        """Metodo que corre en cada Frame del juego"""

        #Obtenemos los limites de la mesa, red, paddle y las velocidas del paddle en x,y,z
        table_limits = table.get_limits()
        net_limits = net.get_limits()
        paddle_limits = paddle.get.limits()
        paddle_velocities = (paddle.vx, paddle.vy, paddle.vz)

        #Llama al metodo movement_update del modulo physics y le pasa los limites
        self.physics._movement_update(table_limits, net_limits)

        #Sincroniza las variables visuales con los nuevos valores de las fisicas
        self.x = self.physics.position.x
        self.y = self.physics.position.y
        self.z = self.physics.position.z