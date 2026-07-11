import pygame as py
import config
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .renderer import Renderer
    from .pseudo_3D import Pseudo3D
    from ..resources.resource_manager import ResourceManager
    from ..entities import *

class WorldRenderer:
    def __init__(self, resource_manager: "ResourceManager", renderer: "Renderer", pseudo_3D: "Pseudo3D") -> None:
        self.resource_manager = resource_manager
        self.renderer = renderer
        self.pseudo_3D = pseudo_3D  

        self._render_queue = []

    def clear_queue(self):
        """Limpia la cola al inicio de cada fotograma"""
        self._render_queue.clear()

    def add_xz_element(self, element_x: int, element_y: int, element_z: int, below_surface_z: int, element_width: int, element_depth: int, state_name: str, texture_key: str, surface=None, angle=None):
        """Registra una entidad vertical para que sea dibujada, mediante sprite stacking o como sprite normal, junto a su sombra eliptica"""
        self._render_queue.append({
            "sort_y": element_y,
            "type": "xz",
            "data": (element_x, element_y, element_z, below_surface_z, element_width, element_depth, state_name, texture_key, surface, angle)
        })

    def add_xy_element(self, element_x: int, element_y: int, element_z: int, element_half_width: int, element_half_depth: int, state_name: str, texture_key: str, surface: py.Surface):
        """Registra un plano paralelo al eje xy del mundo matematico"""
        z_priority = element_y + 1000 #AAREGLA
        self._render_queue.append({
            "sort_y": z_priority,
            "type": "xy",
            "data": (element_x, element_y, element_z, element_half_width, element_half_depth, state_name, texture_key, surface)
        })

    def render_world(self, ) -> None:
        """ 
        Dibuja el mundo con los metodos gráficos privados después de ordenar la cola de mayor a menor profundidad
        """
        #Ordenamiento: el elemento con mayor sort_y se dibuja primero
        self._render_queue.sort(key=lambda item: item["sort_y"], reverse=True)

        #recorrido de la cola ordenada
        for item in self._render_queue:
            type = item["type"]
            data = item["data"]

            if type == "xz":
                self._render_xz_element(*data)
            elif type == "xy":
                self._render_xy_element(*data)

        #METODOS PRIVADOS DE DIBUJO

    def _render_xz_element(self, element_x, element_y, element_z, below_surface_z, element_width, element_depth, state_name, texture_key, surface, angle):
        """
        Dibuja en pantalla una entidad vertical (mediante sprite stacking o como sprite normal) junto a su sombra su sombra
        """
        element_sx, element_sy, element_scale = self.pseudo_3D.world_to_screen(element_x, element_y, element_z)
        shadow_sx, shadow_sy, _ = self.pseudo_3D.world_to_screen(element_x, element_y, below_surface_z)

        shadow_width, shadow_height, shadow_alpha = self.pseudo_3D.get_shadow_properties(element_z, element_scale, element_width, element_depth)

        element_screen_data = (element_sx, element_sy, element_scale)
        shadow_screen_data = ((shadow_sx, shadow_sy, shadow_width, shadow_height), shadow_alpha)

        self.renderer.render_ellipse(*shadow_screen_data, angle)

        if angle is not None:
            layers = self.resource_manager.get_sprite_stack(state_name, texture_key, angle)
            self.renderer.render_sprite_stack(layers, *element_screen_data)
        elif surface is not None:
            self.renderer.render_sprite(surface, *element_screen_data)
        else:
            texture = self.resource_manager.get_texture(state_name, texture_key)
            self.renderer.render_sprite(texture, *element_screen_data)



    def _render_xy_element(self, element_x, element_y, element_z, element_half_width, element_half_depth, state_name, texture_key, surface):
        """
        Dibujar un poligono paralelo al plano xy del mundo matematico en pantalla, a partir de lineas escaladas de un sprite
        Para mejor rendimiento solo hace los blits de cada tira o linea la primera vez, luego guarda en caché como un surface completo del tamaño de la pantalla
        """
        cache_key = f"perspective_{state_name}_{texture_key}"
        perspective_surface = self.resource_manager.cache.get(cache_key)

        if perspective_surface is None:
            temp_canvas = py.Surface(config.WINDOW_SIZE, py.SRCALPHA)
            sprite_height = surface.get_height()

            y_max = element_y + element_half_depth
            y_min = element_y - element_half_depth

            element_width = element_half_width * 2

            for line in range(sprite_height):
                #Factor de 0.0 - 1.0 que representa el avance de las lineas del sprite
                height_percentage = line / sprite_height
                y_line = y_max - (y_max - y_min) * height_percentage

                line_sx, line_sy, line_scale = self.pseudo_3D.world_to_screen(element_x, y_line, element_z)
                if line_scale <= 0:
                    continue
                #Early culling para las lineas horizontales(si estan por encima o debajo de la altura de la pantalla,
                #el margen de 5 pixeles protege de borrar lineas que se escalen mas altas y sean parcialmente visibles)
                if line_sy < -5 or line_sy > config.WINDOW_HEIGHT + 5:
                    continue

                line_width = element_width * line_scale
                #Early culling para las lineas horizontales(si estan por fuera del ancho de la pantalla)
                if (line_sx + line_width // 2) < 0 or (line_sx - line_width // 2) > config.WINDOW_WIDTH:
                   continue

                scaled_strip = self.resource_manager.get_scaled_strip(surface, texture_key, line, line_width, 1)

                strip_w = scaled_strip.get_width()
                strip_h = scaled_strip.get_height()
                final_sx = line_sx - strip_w // 2
                final_sy = line_sy - strip_h // 2

                temp_canvas.blit(scaled_strip, (final_sx, final_sy))
            
            self.resource_manager.cache.save(cache_key, temp_canvas)
            perspective_surface = temp_canvas

        self.renderer.render_sprite(perspective_surface, config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2)