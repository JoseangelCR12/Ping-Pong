import pygame as py

class Renderer:
    def __init__(self, screen: py.Surface) -> None:
        self.screen = screen

    def render_sprite(self, texture: py.Surface, x: float, y:float) -> None:
        """Dibuja un sprite 2D comun directamente"""
        self.screen.blit(texture, (int(x), int(y)))

    def render_sprite_stack(self, rotated_layers: list[py.Surface], screen_x: float, screen_y: float, scale) -> None:
        """Dibuja las capas ya rotadas desde la caché aplicando el desfase vertical para el efecto pseudo 3d, asi como el escalado para sensacion de profundidad"""
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
            
        #Blint en la pantalla centrando el resultado
        final_x = int(screen_x) - (new_w // 2)
        final_y = int(screen_y) - (new_h // 2)
        self.screen.blit(scaled_stack, (final_x, final_y))
