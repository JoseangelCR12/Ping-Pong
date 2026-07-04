import config
class Table():
    def __init__(self, x_center, y_center, z = 0) -> None:
        #Coordenadas en el espacio 3D matematico
        self.x = x_center
        self.y = y_center
        self.z = z
        
        #Dimensiones
        self.half_width = config.HALF_TABLE_WIDTH
        self.half_length = config.HALF_TABLE_LENGTH
        self.thickness = config.TABLE_THICKNESS

        #limites de la collision box
        self._limits = (self.x - self.half_width, self.x + self.half_width,
                        self.y - self.half_length, self.y + self.half_length,
                        self.z - self.thickness, self.z)
        
    def get_limits(self):
        """Retorna los limites fijos de la mesa (min_x, max_x, min_y, max_y, min_z, max_z)"""
        return self._limits

   