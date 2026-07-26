import pygame as py
import config
from ..utils.pseudo_3D import Pseudo3D
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .renderer import Renderer
    from ..resources.resource_manager import ResourceManager
    from ..entities import *

class WorldRenderer:
    def __init__(self, resource_manager: "ResourceManager", renderer: "Renderer") -> None:
        self.resource_manager = resource_manager
        self.renderer = renderer 

        self._render_queue = []

        #Valores de prioridades y ajustes para que un objeto superior plano xy cubra a uno inferior xz y normalmente los planos quede debajo
        self.z_priority = 1000
        #superficie principal para sombras, actua como mascara de recorte, cuando un plano xy tenga shadows_on en True, se guarda aqui una mascara de recorte
        self.element_surface = None

    def clear_queue(self):
        """Limpia la cola al inicio de cada fotograma"""
        self._render_queue.clear()

    def add_xz_element(self, element_x: int, element_y: int, element_z: int, state_name: str, texture_key: str, plane_surface_z: int, plane_min_y: int, element_depth: int, element_height: int, is_stack: bool=False, angle=0, surface=None, element_width=None, has_shadow: bool=True):
        """
        Registra una entidad vertical para que sea dibujada, mediante sprite stacking o como sprite normal, junto a su sombra eliptica si se da una superficie inferior, si dicha superficie es superior se toma como referencia de techo
        """
        #Prioridad normal de los elementos verticales
        render_priority = element_y 
        
        #Bloque para que los elementos que bajen de la altura del plano xy de referencia sean dibujados detras de dicho plano
        element_min_z = element_z - element_height // 2
        element_max_y = element_y + element_depth // 2
        
            #Si la parte inferior de la altura del elemento baja de la z del plano
            #Y la parte mas alejada de dicho elemento esta mas alejada de nosotros que la parte mas cercana del plano de referencia
        if element_min_z < plane_surface_z and element_max_y > plane_min_y:
            render_priority += (self.z_priority * 1.5)
               
        self._render_queue.append({
            "sort_y": render_priority,
            "type": "xz",
            "data": (element_x, element_y, element_z, state_name, texture_key, plane_surface_z, is_stack, angle, surface, element_width, element_depth, has_shadow)
        })

    def add_xy_element(self, element_x: int, element_y: int, element_z: int, element_half_width: int, element_half_depth: int, state_name: str, texture_key: str, plane_surface_z: int, surface: py.Surface, shadow_surface=None, shadows_on_top=False):
        """Registra un plano paralelo al eje xy del mundo matematico, junto a su sombra cuadrilateral si se da una superficie plana inferior"""
        render_priority = element_y + self.z_priority #Prioridad para que las superficies horizontales se dibujen primero (normalmente suelos o mesas)
        self._render_queue.append({
            "sort_y": render_priority,
            "type": "xy",
            "data": (element_x, element_y, element_z, element_half_width, element_half_depth, state_name, texture_key, surface, shadows_on_top),
        })
        #Si el elemento tiene sombra, la añadimos a la cola
        if element_z > plane_surface_z:          
            self._render_queue.append({
            "sort_y": render_priority + 1, #Para que nunca quede por encima de la entidad le sumamos 1
            "type": "xy",
            "data": (element_x, element_y, plane_surface_z, element_half_width, element_half_depth, state_name, f"shadow_{texture_key}", shadow_surface)
            })

    def render_world(self) -> None:
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

    def _render_xz_element(self, element_x, element_y, element_z, state_name, texture_key, plane_surface_z, is_stack, angle, surface, element_width, element_depth, has_shadow):
        """
        Dibuja en pantalla una entidad vertical (mediante sprite stacking o como sprite normal) junto a su sombra 
        """
        element_sx, element_sy, element_scale = Pseudo3D.world_to_screen(element_x, element_y, element_z)
        element_screen_data = (element_sx, element_sy, element_scale)

        #Bloque para las sombras
        if plane_surface_z < element_z and self.element_surface is not None and has_shadow == True: #Si hay una superficie receptora guardada, recortamos las sombras
            shadow_sx = element_sx
            delta_sy = element_scale * (element_z - plane_surface_z) 
            shadow_sy = element_sy + delta_sy  #igual matematicamente a: shadow_sx, shadow_sy, _ = Pseudo3D.world_to_screen(element_x, element_y, plane_surface_z)
            shadow_width, shadow_height, shadow_alpha = Pseudo3D.get_shadow_properties(element_z, element_scale, element_width, element_depth)
            shadow_screen_data = ((shadow_sx, shadow_sy, shadow_width, shadow_height), shadow_alpha)

            #surface temporal para hacer blit de las sombras, del tamaño de la pantalla
            shadow_canvas = py.Surface(config.WINDOW_SIZE, py.SRCALPHA)
            self.renderer.render_ellipse(shadow_canvas, *shadow_screen_data, angle)

            #Hacemos el blend_rgba_min de la superficie de mascara de recorte (completamente blanca), sobre las sombras
            shadow_canvas.blit(self.element_surface, (0, 0), None, special_flags=py.BLEND_RGBA_MIN)
        
            #Dibujamos en pantalla
            center = config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2
            self.renderer.render_sprite(shadow_canvas, *center)
   
        if is_stack:
            layers = self.resource_manager.get_sprite_stack(state_name, texture_key, angle)
            self.renderer.render_sprite_stack(layers, *element_screen_data)
        elif surface is not None:
            self.renderer.render_sprite(surface, *element_screen_data)
        else:
            texture = self.resource_manager.get_texture(state_name, texture_key)
            self.renderer.render_sprite(texture, *element_screen_data)

    def _render_xy_element(self, element_x: int, element_y: int, element_z: int, element_half_width: int, element_half_depth: int, state_name: str, texture_key: str, surface: py.Surface, shadows_on_top: bool=False):
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

                line_sx, line_sy, line_scale = Pseudo3D.world_to_screen(element_x, int(y_line), element_z)
        
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

                scaled_strip = self.resource_manager.get_scaled_strip(surface, texture_key, line, line_width, 1.5)

                strip_w = scaled_strip.get_width()
                final_sx = line_sx - strip_w // 2
                final_sy = line_sy - (1 + height_percentage) // 2 #de esta forma los pixeles se van solapando, se evitan los huecos entre lineas horizontales

                temp_canvas.blit(scaled_strip, (final_sx, final_sy))
            
            if texture_key.startswith("shadow_"):
                perspective_surface = temp_canvas.set_alpha(100)
                
            if shadows_on_top == True: #Si el plano tiene shadow_on_top activo
                element_mask = py.mask.from_surface(temp_canvas)
                color = (255, 255, 255, 255) 
                self.element_surface = element_mask.to_surface( #Superficie que actuará como la mascara de recorte para las sombras
                    setcolor=color, unsetcolor=(0, 0, 0, 0)
                )

            perspective_surface = temp_canvas
            self.resource_manager.cache.save(cache_key, perspective_surface)

        self.renderer.render_sprite(perspective_surface, config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2)
    