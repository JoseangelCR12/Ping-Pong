import config
from ..core import settings
class Pseudo3D:
    def __init__(self):
        #Punto de fuga
        self.vanishing_sx = config.WINDOW_WIDTH // 2


    def world_to_screen(self, world_x: int, world_y: int, world_z: int):
        """produce ubicaciones para la pantalla a partir del espacio 3d simulado matematicamente"""   

        #Buscamos en los ajustes de la camara
        horizon_line = settings.data["horizon_line"]
        camera_depth = settings.data["camera_depth"]
        camera_height = settings.data["camera_height"]
        focal_length = settings.data["focal_length"]
        k_padding = settings.data["k_padding"]

        relative_y = world_y - camera_depth

        #restricción para evitar division por cero y scale (-)
        if relative_y + k_padding <= 0:
            return 0, 0, 0
        
        #Calculamos la escala de tamaño basada en la profundidad (Y)
        scale = focal_length / (relative_y + (k_padding))
        
        #el objeto se debe desviar lateralmente hacia el punto de fuga a medida que se aleja de nosotros
        screen_x = self.vanishing_sx + (world_x * scale) 


        #se multiplica la profundidad Y y la altura Z por la escala para disminuir el movimiento en la distancia
        raw_sy = horizon_line + (camera_height * scale)  # Las imagenes se desplaza hacia abajo a medida que la cámara se eleva  
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


