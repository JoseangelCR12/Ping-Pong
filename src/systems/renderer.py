import pygame as py

class Renderer:
    def __init__(self, screen: py.Surface) -> None:
        self.screen = screen

    def render_sprite(self, texture: py.Surface, x: int, y:int, scale = None) -> None:
        """Dibuja un sprite 2D comun directamente, centrado"""
        texture_w = texture.get_width()
        texture_h = texture.get_height()
        
        if scale is not None:
            texture_w = int(texture_w * scale)
            texture_h = int(texture_h * scale)
            texture = py.transform.scale(texture, (texture_w, texture_h))
            
        final_x = x - texture_w // 2
        final_y = y - texture_h // 2
        self.screen.blit(texture, (final_x, final_y))

    def render_sprite_stack(self, rotated_layers: list[py.Surface], screen_x: int, screen_y: int, scale: float) -> None:
        """
        Dibuja las capas ya rotadas desde la caché aplicando el desfase vertical para el efecto pseudo 3d, asi como el escalado para sensacion de profundidad
        Dibuja en pantalla el sprite apilado centrado en x e y
        """
        layer_w = rotated_layers[0].get_width()
        layer_h = rotated_layers[0].get_height()
        total_layers = len(rotated_layers)

        #El alto de la superficie temporal debe considerar el desfase de todas las capas
        stack_surface = py.Surface((layer_w, layer_h + len(rotated_layers)), py.SRCALPHA)

        #Empezamos la base de la superficie distanciando por el numero de capas (vamos subiendo con cada capa usando escala 1)
        start_y = total_layers

        #Dibujamos las capas en nuestra surface temporal
        for i, layer in enumerate(rotated_layers):
            stack_surface.blit(layer, (0, start_y - i))

        #Escalamos el bloque completo
        new_w = int(stack_surface.get_width() * scale)
        new_h = int(stack_surface.get_height() * scale)
        scaled_stack = py.transform.scale(stack_surface, (new_w, new_h)) 
            
        #Blint en la pantalla centrando el resultado en x e y
        final_x = (screen_x) - (new_w // 2)
        final_y = (screen_y) - (new_h // 2)
        self.screen.blit(scaled_stack, (final_x, final_y))

    def render_ellipse(self, canvas, rect: tuple[int, int, int, int], alpha: int, angle: int = 0) -> None:
        """Dibuja una elipse negra centrada dada una tupla de coordenadas (x, y, width, height), y una opacidad"""
        #Dibujamos en una surface temporal
        temp_surface = py.Surface((rect[2], rect[3]), py.SRCALPHA)
        color_alpha = (0, 0, 0, alpha)  # Color negro con opacidad variable
        py.draw.ellipse(temp_surface, color_alpha, (0, 0, rect[2], rect[3]))

        #Si el angulo no es cero rotamos la superficie
        if angle != 0:
            temp_surface = py.transform.rotate(temp_surface, angle)
        
        #Calculamos el rect para centrarlo y que no se mueva raro si rota
        surface_rect = temp_surface.get_rect()
        surface_rect.center = (rect[0], rect[1])
        
        canvas.blit(temp_surface, (surface_rect))

    def render_rectangle(self, rect: tuple[int, int, int, int], alpha: int, angle: int = 0) -> None:
        """Dibuja un rectangulo negro centrado dada una tupla de coordenadas (x, y, width, height), y una opacidad"""
        #Dibujamos en una surface temporal
        temp_surface = py.Surface((rect[2], rect[3]), py.SRCALPHA)
        color_alpha = (0, 0, 0, alpha)  # Color negro con opacidad variable
        py.draw.rect(temp_surface, color_alpha, (0, 0, rect[2], rect[3]))

        #Si el angulo no es cero rotamos la superficie
        if angle != 0:
            temp_surface = py.transform.rotate(temp_surface, angle)

        #Calculamos el rect para centrarlo y que no se mueva raro si rota
        surface_rect = temp_surface.get_rect()
        surface_rect.center = (rect[0], rect[1])

        self.screen.blit(temp_surface, (surface_rect))


    