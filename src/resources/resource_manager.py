import pygame as py
from ..utils.paths import get_asset_path
from .assets_def import ASSETS_DICT
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .cache_manager import CacheManager

class ResourceManager:
    def __init__(self, cache: "CacheManager"):       
        self.cache = cache
        self.ASSETS_DICT = ASSETS_DICT
        
    #METODOS PUBLICOS PRINCIPALES
    
    def get_texture(self, state_name, texture_key) -> py.Surface:
        """
        Devuelve una superficie de pygame, busca en los atributos del singleton ASSETS_DICT
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

    def get_sound(self, state_name: str, sound_key: str) -> py.mixer.Sound:
            """
            Devuelve un sound busca en los atributos del singleton ASSETS_DICT
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
        state_data = getattr(self.ASSETS_DICT, state_name, {})

        # Extraemos la ruta de la categoria dada del estado
        relative_path = state_data.get(category,{}).get(key)

        # Si no esta se busca globalmente
        if not relative_path:
            global_data = getattr(self.ASSETS_DICT, "GLOBAL", {})
            relative_path = global_data.get(category,{}).get(key)
                
        #Si no se encuentra en ningun lado
        if not relative_path:
            raise FileNotFoundError(f"No se encontró '{key}' de la categoria '{category}' en '{state_name}' ni en 'GLOBAL'")
        
        return relative_path
    
    def _load_asset(self, state_name: str, category: str, key: str, load_function: Any) -> Any:
        """Consigue la ruta, la limpia(para que sea independiente del OS) y ejecuta la carga de Pygame"""
        relative_path = self._get_path_from_dict(state_name, category, key)
        clean_path = get_asset_path(relative_path)

        #ejecuta py.image.load o py.mixer.Sound segun la funcion recibida
        return load_function(clean_path)