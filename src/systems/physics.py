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
        self.acceleration.ax = 0.0
        self.acceleration.ay = 0.0
        self.restitution = config.BALL_RESTITUTION

    def _gravity(self):

        """Aplica la Gravedad en la velocidad"""

        self.speed.z -= self.gravity / 60.0 
    
    def _apply_acceleration(self):

        """Aplica la aceleracion en la velocidad"""

        self.speed.x += self.acceleration.ax
        self.speed.y += self.acceleration.ay

    def _table_bounce(self, table_limits):   
    
    """Calcula la colision con la mesa y actualiza la velocidad de la pelota"""
        
        #Limites de la mesa
        mintable_x, maxtable_x, mintable_y, maxtable_y, mintable_z, maxtable_z = table_limits
        #Limites de Clampeo
        is_withing_x = mintable_x <= self.position.x <= maxtable_x
        is_withing_y = mintable_y <= self.position.y <= maxtable_y  
        has_hit_surface = mintable_z <= self.position.z <= maxtable_z 

        #Aplicando el impacto con la mesa si la pelota esta dentro de los limites de la mesa
        if is_withing_x and is_withing_y and has_hit_surface:
            self.position.z  = maxtable_z
            self.speed.z *= -self.restitution


    def _floor_bounce (self):
        floor_z = config.FLOOR_Z

    def _movement_update(self):
        """Usa el metodo gravity y apply_acceleration para actualizar la posicion"""
        self._gravity()
        self._apply_acceleration()
        self._table_bounce(table_limits)
        self.position.x += self.speed.x
        self.position.y += self.speed.y
        self.position.z += self.speed.z 
