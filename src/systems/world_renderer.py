import pygame as py
import config
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .renderer import Renderer
    from .pseudo_3D import Pseudo3D
    from ..resources.resource_manager import ResourceManager

class WorldRenderer:
    def __init__(self, resource_manager: "ResourceManager", renderer: "Renderer", pseudo_3D: "Pseudo3D") -> None:
        self.resource_manager = resource_manager
        self.renderer = renderer
        self.pseudo_3D = pseudo_3D  
    
    def render_xz_entity(self, entity_x, entity_y, entity_z, surface_z, entity_width, entity_depth, state_name, texture_key, angle):
        """
        Dibuja en pantalla una entidad vertical (mediante sprite stacking) y su sombra
        """
        entity_sx, entity_sy, entity_scale = self.pseudo_3D.world_to_screen(entity_x, entity_y, entity_z)
        shadow_sx, shadow_sy, _ = self.pseudo_3D.world_to_screen(entity_x, entity_y, surface_z)

        shadow_width, shadow_height, shadow_alpha = self.pseudo_3D.get_shadow_properties(entity_z, entity_scale, entity_width, entity_depth)

        entity_screen_data = (entity_sx, entity_sy, entity_scale)
        shadow_screen_data = ((shadow_sx, shadow_sy, shadow_width, shadow_height), shadow_alpha)

        self.renderer.render_ellipse(*shadow_screen_data, angle)

        layers = self.resource_manager.get_sprite_stack(state_name, texture_key, angle)
        self.renderer.render_sprite_stack(layers, *entity_screen_data)


    def render_xy_polygon(self, polygon_x, polygon_y, polygon_z, polygon_half_width, polygon_half_depth, surface, state_name, texture_key):
        """
        Dibujar un poligono paralelo al plano xy del mundo matematico en pantalla, a partir de lineas escaladas de un sprite
        Para mejor rendimiento solo hace los blits de cada tira o linea la primera vez, luego guarda en caché como un surface completo del tamaño de la pantalla
        """
        cache_key = f"perspective_{state_name}_{texture_key}_{polygon_x}_{polygon_y}_{polygon_z}_{polygon_half_width}_{polygon_half_depth}"
        perspective_surface = self.resource_manager.cache.get(cache_key)

        if perspective_surface is None:
            temp_canvas = py.Surface(config.WINDOW_SIZE, py.SRCALPHA)
            print("jai papa")
            sprite_height = surface.get_height()

            y_max = polygon_y + polygon_half_depth
            y_min = polygon_y - polygon_half_depth

            polygon_width = polygon_half_width * 2

            for line in range(sprite_height):
                #Factor de 0.0 - 1.0 que representa el avance de las lineas del sprite
                height_percentage = line / sprite_height
                y_line = y_max - (y_max - y_min) * height_percentage

                line_sx, line_sy, line_scale = self.pseudo_3D.world_to_screen(polygon_x, y_line, polygon_z)
                if line_scale <= 0:
                    continue
                #Early culling para las lineas horizontales(si estan por encima o debajo de la altura de la pantalla,
                #el margen de 5 pixeles protege de borrar lineas que se escalen mas altas y sean parcialmente visibles)
                if line_sy < -5 or line_sy > config.WINDOW_HEIGHT + 5:
                    continue

                line_width = polygon_width * line_scale
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