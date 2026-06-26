import config
class Pseudo3D:
    def __init__(self):
        #Horizonte y punto de fuga
        self.horizon = config.HORIZON_LINE_Y
        self.vanishing_x = config.TABLE_MIDDLE_X

    def world_to_screen(self, world_x, world_y, world_z, asset_width=0, asset_height=0):
        #produce ubicaciones para la pantalla a partir de nuestro 3d simulado matematicamente
        #Para evitar division por 0 o escalas demasiado grandes
        if world_y <= 1:
            world_y = 1

        #Calculamos la escala de tamaño basada en la profundidad (Y)
        scale = world_y / config.FOCAL_LENGTH 

        #el objeto se debe desviar lateralmente hacia el punto de fuga a medida que se aleja de nosotros
        distance_x = world_x - self.vanishing_x
        screen_x = self.vanishing_x + (distance_x * scale) -((asset_width * scale) / 2)

        #se multiplica la profundidad Y y la altura Z por la escala para disminuir el movimiento en la distancia
        screen_y = self.horizon + (world_y * scale) - (world_z * scale) - ((asset_height * scale) / 2)
        
        return int(screen_x), int(screen_y), scale

        
