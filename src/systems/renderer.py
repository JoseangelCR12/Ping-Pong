import pygame as py
import config

class Renderer:
    def __init__(self, screen: py.Surface) -> None:
        self.screen = screen

    def render_sprite(self, texture: py.Surface, x: float, y:float) -> None:
        """Dibuja un sprite 2D comun directamente"""
        self.screen.blit(texture, (int(x), int(y)))

    def render_sprite_stack(self, rotated_layers: list[py.Surface], screen_x: float, screen_y: float, scale: float) -> None:
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
        final_x = int(screen_x) - (new_w // 2)
        final_y = int(screen_y) - (new_h // 2)
        self.screen.blit(scaled_stack, (final_x, final_y))

    def render_ellipse(self, rect: tuple[int, int, int, int], alpha: int, angle: int) -> None:
        """Dibuja una elipse en la pantalla dada una tupla de coordenadas (x, y, width, height), y una opacidad"""
        temp_surface = py.Surface((rect[2], rect[3]), py.SRCALPHA)
        color_alpha = (0, 0, 0, alpha)  # Color negro con opacidad variable
        py.draw.ellipse(temp_surface, color_alpha, (0, 0, rect[2], rect[3]))
        temp_surface = py.transform.rotate(temp_surface, angle)
        self.screen.blit(temp_surface, (rect[0], rect[1]))

    def render_px (self, rect: tuple[int, int, int, int, int, int]):
        """Dibuja un pixel en la pantalla, para debug"""
        infL, supR, supL, infR, Msy, mSY = rect
        py.draw.line(self.screen, (0, 0, 0), (infL, Msy), (infL, Msy))
        py.draw.line(self.screen, (0, 0, 0), (supR, mSY), (supR, mSY))
        py.draw.line(self.screen, (0, 0, 0), (supL, mSY), (supL, mSY))
        py.draw.line(self.screen, (0, 0, 0), (infR, Msy), (infR, Msy))


    def render_by_scanlines(self, screen_points: tuple[int, int, int, int, int], texture_surface: py.Surface):
        """
        A partir de las esquinas superior e inferior izquierdas y el centro, dibuja un trapecio equilatero cuyo lado menor está arriba
        Dibuja una superficie que simula profundidad estirando lineas horizontales de la textura original
        """
        inf_x, sup_x, min_y, max_y, x_center = screen_points
        screen_height = max_y - min_y
        short_width = 2 * (x_center - sup_x)
        delta_width = 2 * (sup_x - inf_x)
        if delta_width == 0:
            return

        #Rango vertical del trapecio
        y_start = max(0, min_y)
        y_end = min(config.WINDOW_HEIGHT, max_y)
        texture_w, texture_h = texture_surface.get_size()

        scale = texture_h / (screen_height+1)  # Escala para mapear la textura a la altura del trapecio
        

        #Renderizado fila por fila
        for screen_y in range(y_start, y_end + 1):
            #Calculamos la proporcion de la fila actual en el rango vertical
            proportion = (screen_y - min_y) / (max_y - min_y)
            #Interpolamos el ancho de la fila actual entre los dos anchos del trapecio
            current_width = int(short_width + proportion * delta_width)
            #Calculamos la coordenada X inicial para centrar la fila
            start_x = int(x_center - current_width / 2)

            #Calculamos la coordenada Y correspondiente en la textura original
            texture_y = (screen_y - min_y) * scale
            
            #Extraemos la fila de pixeles de la textura original
            row_surface = py.Surface((texture_w, 1), py.SRCALPHA)
            row_surface.blit(texture_surface, (0, 0), (0, texture_y, texture_w, 1))
            #Escalamos la fila al ancho actual del trapecio
            scaled_row = py.transform.scale(row_surface, (current_width, 1))
            #Blint en la pantalla
            self.screen.blit(scaled_row, (start_x, screen_y))
        
