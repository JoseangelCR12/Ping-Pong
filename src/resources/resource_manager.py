import pygame as py
import os
from .assets_def import ASSETS_DICT

class ResourceManager:
    def __init__(self, audio, renderer, cache):
        self._textures = {}
        self._sounds = {}

        self.ASSETS_DICT = ASSETS_DICT
        
    def get_texture(self, state_name, texture_key):
        """
        Devuelve una superficie de pygame, busca en los atributos del Singleton ASSETS_DICT
        """
        # Creamos una clave para el cache combinando el nombre del estado y el de la textura
        cache_key = f"{state_name}_{texture_key}"
        if cache_key in self._textures:
            return self._textures[cache_key]
        
        # Buscamos el atributo del estado en nuestro singleton
        state_data = getattr(self.ASSETS_DICT, state_name, {})

        # Extraemos la ruta de la seccion de sprites del estado
        relative_path = state_data.get("sprites",{}).get(texture_key)

        # Si no esta se busca globalmente
        if not relative_path:
            global_data = getattr(self.ASSETS_DICT, "GLOBAL", {})
            relative_path = global_data.get("sprites",{}).get(texture_key)
        
        # Si no existe en ningun lado
        if not relative_path:
            print(f"NO EXITE LA TEXTURA '{texture_key}' en '{state_name}' ni en 'GLOBAL'")
        
        if os.path.exists(relative_path):
            surface = py.image.load(relative_path).convert_alpha()
            self._textures[cache_key] = surface
            return surface
        else:
            print(f"archivo no encontrado en ruta: {relative_path}")
            return None

    def get_sound(self, state_name, sound_key):
            """
            Devuelve un SFX busca en los atributos del Singleton ASSETS_DICT
            """
            # Creamos una clave para el cache combinando el nombre del estado y el de la textura
            cache_key = f"{state_name}_{sound_key}"
            if cache_key in self._sounds:
                return self._sounds[cache_key]
            
            # Buscamos el atributo del estado en nuestro singleton
            state_data = getattr(self.ASSETS_DICT, state_name, {})

            # Extraemos la ruta de la seccion de sfx del estado
            relative_path = state_data.get("sfx",{}).get(sound_key)

            # Si no esta se busca globalmente
            if not relative_path:
                global_data = getattr(self.ASSETS_DICT, "GLOBAL", {})
                relative_path = global_data.get("sfx",{}).get(sound_key)
            
            # Si no existe en ningun lado
            if not relative_path:
                print(f"NO EXITE EL SFX '{sound_key}' en '{state_name}' ni en 'GLOBAL'")
            
            if os.path.exists(relative_path):
                sfx = py.mixer.Sound(relative_path)
                self._sounds[cache_key] = sfx
                return sfx
            else:
                print(f"archivo no encontrado en ruta: {relative_path}")
                return None

    def get_music_path(self, state_name, music_key):
        """
        Para musica de fondo, solo devuelve la ruta porque no se guarda en RAM, pygame hace streaming del archivo desde cpu
        """
        state_data = getattr(self.ASSETS_DICT, state_name, {})

        # Extraemos la ruta de la seccion de music del estado
        relative_path = state_data.get("music",{}).get(music_key)

        # Si no esta se busca globalmente
        if not relative_path:
            global_data = getattr(self.ASSETS_DICT, "GLOBAL", {})
            relative_path = global_data.get("music",{}).get(music_key)
            
        # Si no existe en ningun lado
        if not relative_path:
            print(f"NO EXITE LA MUSICA '{music_key}' en '{state_name}' ni en 'GLOBAL'")
            
        if os.path.exists(relative_path):
            return relative_path 
                
        else:
            print(f"archivo no encontrado en ruta: {relative_path}")
            return None



    