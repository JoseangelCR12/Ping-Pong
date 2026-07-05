import config
import math
class Pseudo3D:
    def __init__(self):
        #Punto de fuga
        self.vanishing_sx = config.WINDOW_WIDTH // 2
        self.vanishing_sy = config.HORIZON_LINE_SY

    def world_to_screen(self, world_x, world_y, world_z):
        """produce ubicaciones para la pantalla a partir del espacio 3d simulado matematicamente"""
        
        relative_y = world_y - config.CAMERA_DEPTH

        #Calculamos la escala de tamaño basada en la profundidad (Y)
        scale = config.FOCAL_LENGTH / (relative_y + (config.K_PADDING))
        
        #el objeto se debe desviar lateralmente hacia el punto de fuga a medida que se aleja de nosotros
        screen_x = self.vanishing_sx + (world_x * scale) 


        #se multiplica la profundidad Y y la altura Z por la escala para disminuir el movimiento en la distancia
        raw_sy = self.vanishing_sy + (config.CAMERA_HEIGHT * scale)  # La línea de la mesa se desplaza hacia abajo a medida que la cámara se eleva  
        screen_y = raw_sy - (world_z * scale)

        return int(screen_x), int(screen_y), scale
        
    def get_shadow_properties(self, world_z, base_scale, sprite_width, sprite_depth):
        """Calcula el tamaño y la opacidad de la sombra en función de la altura del objeto (world_z) y la escala base"""
        height_factor = max(0.5, 1 - (world_z / 300))
        shadow_scale = base_scale * height_factor
        BASE_OPACITY = 210
        shadow_opacity = int(BASE_OPACITY * height_factor)
        shadow_width = int(sprite_width * shadow_scale)
        shadow_depth = int(sprite_depth * shadow_scale)

        return shadow_width, shadow_depth, shadow_opacity

    def mouse_to_world(self, mouse_x, mouse_y):
        """
        Traduce las coordenadas 2D del mouse a coordenadas 3D para la raqueta del jugador (world_x, world_y)
        """
    
        #Calculo de la profundidad (world_y)
        world_y = config.NET_Y - (mouse_y * config.NET_Y / config.WINDOW_HEIGHT)

        #Calculo de world_x
        x_proportion = config.HALF_TABLE_WIDTH / (self.vanishing_sx)  # Proporción de la mitad del ancho de la mesa respecto al punto de fuga
        world_x = (mouse_x - self.vanishing_sx) * x_proportion
    
        return world_x, world_y
