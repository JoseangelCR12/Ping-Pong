import config
class Pseudo3D:
    def __init__(self):
        #Punto de fuga
        self.vanishing_sx = config.WINDOW_WIDTH // 2
        self.vanishing_sy = config.HORIZON_LINE_SY  

    def world_to_screen(self, world_x: int, world_y: int, world_z: int):
        """produce ubicaciones para la pantalla a partir del espacio 3d simulado matematicamente"""      
        relative_y = world_y - config.CAMERA_DEPTH

        #restricción para evitar division por cero y scale (-)
        if relative_y + config.K_PADDING <= 0:
            return 0, 0, 0
        
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


