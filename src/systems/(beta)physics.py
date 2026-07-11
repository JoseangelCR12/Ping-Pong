import config

class Physics:

    """Agarramos las Variables de posicion y velocidad del objeto e inicializamos la gravedad, aceleracion y restitucion"""

    def __init__(self, x = 0.0, y = 0.0, z = 0.0, vx = 0.0, vy = 0.0, vz = 0.0):

        self.speed.x = vx
        self.speed.y = vy
        self.speed.z = vz
        self.position.x = x
        self.position.y = y
        self.position.z = z
        self.gravity = config.GRAVITY
        self.restitution = config.BALL_RESTITUTION
        self.net_restitution = config.NET_RESTITUTION
        self.paddle_restitution = config.PADDLE_RESTITUTION
        self.paddle_back_restitution = config.PADDLE_BACK_RESTITUTION
        self.vertical_braking = config.VERTICAL_BRAKING

    def gravity(self):

        """Aplica la Gravedad en la velocidad"""

        self.speed.z -= self.gravity / 60.0 

    def table_bounce(self, table_limits):   
    
        """Calcula la colision con la mesa y actualiza la velocidad de la pelota"""
        
        #Limites de la mesa
        min_table_x, max_table_x, min_table_y, max_table_y, min_table_z, max_table_z = table_limits
    
        #Limites de Clampeo
        is_withing_x = min_table_x <= self.position.x <= max_table_x
        is_withing_y = min_table_y <= self.position.y <= max_table_y  
        has_hit_surface = min_table_z <= self.position.z <= max_table_z 

        #Aplicando el impacto con la mesa si la pelota esta dentro de los limites de la mesa
        if is_withing_x and is_withing_y and has_hit_surface:
                self.position.z  = max_table_z
                self.speed.z *= -self.restitution

    def floor_bounce(self):

        """Inicializamos el piso y aplicamos el rebote"""

        floor_z = config.FLOOR_Z

        #Si la pelota pasa el piso en 1 frame, la regresa al piso y rebota
        if self.position.z <= floor_z:
                self.position.z = floor_z
                self.speed.z *= -self.restitution
                return True
              
        return False

    def net_bounce(self, net_limits):

        """Calcula el Rebote de la pelota con la malla"""

        min_net_x, max_net_x, min_net_y, max_net_y, min_net_z, max_net_z = net_limits
        
        #Comprobando si esta en los limites de la red
        is_withing_x = min_net_x <= self.position.x <= max_net_x
        is_withing_y = min_net_y <= self.position.y <= max_net_y
        is_withing_z = min_net_z <= self.position.z <= max_net_z

        #Si entra en la caja se aplica el impacto
        if is_withing_x and is_withing_y and is_withing_z:
                
        #Si va desde el jugador al cpu
                if self.speed.y > 0:
                        self.position.y = min_net_y

        #Si va desde el cpu al jugador
                else:
                     self.position.y = max_net_y

        #Aplica la restitucion a la pelota
                self.speed.y *= -self.net_restitution

        #Frena un poco su velocidad vertical
                self.speed.z *= self.vertical_braking

    def calculate_entity_vel(self, entity, dt):

        """Metodo que calcula la velocidad de todas las entidades"""

        #Calcula la velocidad de la raqueta en cada frame
        if dt > 0:
            vx = (entity.x - entity.last_x)/ dt
            vy = (entity.y - entity.last_y)/ dt
            vz = (entity.z - entity.last_z)/ dt

        #Guardamos el resultado en los atributos a la entidad
            entity.vx = vx
            entity.vy = vy
            entity.vz = vz

        #Actualiza el historial de la raqueta
            entity.last_x = entity.x
            entity.last_y = entity.y
            entity.last_z = entity.z

            return vx, vy, vz
        
        return 0.0, 0.0, 0.0

    def paddle_bounce(self, paddle, dt):
    
        min_paddle_x, max_paddle_x, min_paddle_y, max_paddle_y, min_paddle_z, max_paddle_z, angle, twiddle = paddle.get_limits()
        paddle_vx, paddle_vy, paddle_vz = self.calculate_entity_vel(paddle, dt)

        is_within_x = min_paddle_x <= self.position.x <= max_paddle_x
        is_within_y = min_paddle_y <= self.position.y <= max_paddle_y
        is_within_z = min_paddle_z <= self.position.z <= max_paddle_z

        if is_within_x and is_within_y and is_within_z:

            if self.speed.y < 0:
                self.position.y = max_paddle_y

            else:
                self.position.y = min_paddle_y

            if twiddle:
                current_restitution = self.paddle_restitution
            else:
                current_restitution = self.paddle_back_restitution
            
            self.speed.y *= -current_restitution

            self.speed.x += paddle_vx * 0.5
            self.speed.y += paddle_vy * 1.0
            self.speed.z += paddle_vz * 0.5

        else:
            self.calculate_entity_vel(paddle, dt)
    
    def movement_update(self, table_limits, net_limits, paddle, dt):

        """Metodo que se encarga de actualizar el movimiento del juego"""

        #Metodo que controla la Gravedad
        self.gravity()

        self.speed.x *= config.FRICTION
        self.speed.y *= config.FRICTION
        #Metodos que se encargan del rebote de la pelota
        self.table_bounce(table_limits)
        self.net_bounce(net_limits)
        self.paddle_bounce(paddle, dt)
        self.floor_bounce()

        #Actualizacion de la posicion en base a la velocidad
        self.position.x += self.speed.x
        self.position.y += self.speed.y
        self.position.z += self.speed.z 
