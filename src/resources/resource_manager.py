import pygame as py
import math
from . import assets_def
from ..core import settings
from ..utils.paths import get_asset_path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .cache_manager import CacheManager

class ResourceManager:
    def __init__(self, cache: "CacheManager"):       
        self.cache = cache
        
    #METODOS PUBLICOS PRINCIPALES
    
    def get_texture(self, state_name, texture_key) -> py.Surface:
        """
        Devuelve una superficie de pygame
        """
        # Creamos una clave para el cache combinando el nombre del estado y el de la textura
        cache_key = f"{state_name}_{texture_key}"
        cached_texture = self.cache.get(cache_key)
        if cached_texture is not None and isinstance(cached_texture, py.Surface) :
            return cached_texture 

        #utilizamos nuestro metodo privado generico
        texture = self._load_asset(state_name, "sprites", texture_key, py.image.load)
        texture = texture.convert_alpha() #Optimizacion de imagenes

        self.cache.save(cache_key, texture)
        return texture
    
    def get_sprite_stack(self, state_name: str, texture_key: str, angle: float) -> list[py.Surface]:
        """Carga bajo demanda las rotaciones de la lista de surfaces del objeto"""
        int_angle = int(angle) % 360
        rotated_cache_key = f"{state_name}_{texture_key}_stack_{int_angle}"

        #Intenta sacar la lista ya rotada desde cache
        cached_rotated = self.cache.get(rotated_cache_key)

        #Validacion para que lo obtenido sea una lista
        if cached_rotated is not None and isinstance(cached_rotated, list):
            return cached_rotated

        #Si es un angulo nuevo tratamos de buscar el angulo 0(la capas sin rotar)
        zero_angle_key = f"{state_name}_{texture_key}_stack_0"
        base_layers = self.cache.get(zero_angle_key)

        #si las capas en angulo 0 no se han cortado aún
        if base_layers is None or not isinstance(base_layers, list):
            #Cargamos la hoja completa usando el metodo generico
            full_sheet = self._load_asset(state_name, "spritesheets", texture_key, py.image.load)
            full_sheet = full_sheet.convert_alpha()

            #Cortamos
            base_layers = []
            size = full_sheet.get_height()
            for i in range(full_sheet.get_width() // size):
                base_layers.append(full_sheet.subsurface((i*size, 0, size, size)))

            self.cache.save(zero_angle_key, base_layers)
        
        if int_angle == 0:
            return base_layers
        
        #Crear el nuevo angulo
        rotated_layers = [py.transform.rotate(layer,int_angle) for layer in base_layers]
        self.cache.save(rotated_cache_key, rotated_layers)
        return rotated_layers       

    def get_scaled_strip(self, texture_surface: py.Surface, texture_key: str, line, line_width, line_height = 1):
        """
        Devuelve un subsurface horizontal (una tira) a partir de un surface
        """
        # Creamos una clave para el cache combinando el nombre del la textura de la que se genera la tira y el indice de la tira
        cache_key = f"{texture_key}_{line}_strip"
        cached_strip = self.cache.get(cache_key)
        if cached_strip is not None and isinstance(cached_strip, py.Surface):
            return cached_strip
        
        sprite_width = texture_surface.get_width()

        rect_subsurface = py.Rect(0, line, sprite_width, line_height)
        subsurface = texture_surface.subsurface(rect_subsurface)

        new_width = math.ceil(line_width)
        new_height = math.ceil(line_height * line_width / sprite_width)
        
        scaled_subsurface = py.transform.scale(subsurface, (new_width, new_height))

        self.cache.save(cache_key, scaled_subsurface)

        return scaled_subsurface

    def get_sound(self, state_name: str, sound_key: str) -> py.mixer.Sound:
        """
        Devuelve un sound (sfx)
        """
        # Creamos una clave para el cache combinando el nombre del estado y el del sonido
        cache_key = f"{state_name}_{sound_key}_sound"
        cached_sound = self.cache.get(cache_key)
        if cached_sound is not None and isinstance(cached_sound, py.mixer.Sound):
            return cached_sound
        
        sound = self._load_asset(state_name, "sound", sound_key, py.mixer.Sound)
        self.cache.save(cache_key, sound)
        return sound

    def get_music_path(self, state_name, music_key):
        """
        Para musica de fondo, solo devuelve la ruta porque no se guarda en RAM, pygame hace streaming del archivo desde cpu
        """
        #usamos nuestro metodo privado
        music_path = self._get_path_from_dict(state_name, "music", music_key)
        return music_path

    
    #METODOS PRIVADOS AUXILIARES
    def _get_path_from_dict(self, state_name: str, category: str, key: str) -> str:
        """Busca la ruta en el estado actual o en GLOBAL"""
        #category puede ser "sprites" "spritesheets" o "audio"
        state_data = getattr(assets_def, state_name, {})

        # Extraemos la ruta de la categoria dada del estado
        relative_path = state_data.get(category,{}).get(key)
        

        # Si no esta se busca globalmente
        if not relative_path:
            global_data = getattr(assets_def, "GLOBAL", {})
            relative_path = global_data.get(category,{}).get(key)
                
        #Si no se encuentra en ningun lado
        if not relative_path:
            raise FileNotFoundError(f"No se encontró '{key}' de la categoria '{category}' en '{state_name}' ni en 'GLOBAL'")
        
        return relative_path
    
    def _load_asset(self, state_name: str, category: str, key: str, load_function: Any) -> Any:
        """Consigue la ruta, la limpia(para que sea independiente del OS) y ejecuta la carga de Pygame"""
        relative_path = self._get_path_from_dict(state_name, category, key)
        
        #Aplicamos el formato del tema
        current_theme = settings.data["theme"]
        formatted_path = relative_path.format(theme=current_theme)

        clean_path = get_asset_path(formatted_path)

        #ejecuta py.image.load o py.mixer.Sound segun la funcion recibida
        return load_function(clean_path)