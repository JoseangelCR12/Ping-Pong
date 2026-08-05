import pygame as py
from ..core.settings import data
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..resources.resource_manager import ResourceManager


class Audio:
    def __init__(self, resource_manager: "ResourceManager") -> None:
        self.resource_manager = resource_manager
        self.current_music_key = None

    #EFECTOS DE SONIDO (SFX), CORTOS Y CARGADOS EN CACHE
    def play_sound(self, state_name: str, sound_key: str) -> None:
        """Pide el sonido al gestor de recursos usando la cache y lo reproduce"""
        try:
            #pedimos el sonido precargado
            sound = self.resource_manager.get_sound(state_name, sound_key)

            if sound:
                #sincronizamos el volumen leyendo los ajustes
                volume = data.get("volume_sfx", 0.7)
                sound.set_volume(volume)

                sound.play()
        
        except Exception as e:
            print(f"Error al reproducir SFX {sound_key} en {state_name}: e")

    #MUSICA DE FONDO, LARGA Y VIA STREAMING 
    def play_music(self, state_name: str, music_key: str, loops: int = -1) -> None:
        #si la musica solicitada ya esta sonando, evitamos reiniciarla
        if self.current_music_key == music_key:
            return
        
        try:
            #Pedimos la ruta al gestor de recursos
            path = self.resource_manager.get_music_path(state_name, music_key)

            #cargamos la pista via streaming
            py.mixer.music.load(path)

            #sincronizamos el volumen del canal
            self.update_music_volume()
            
            #Iniciamos la reproduccion (loops -1 significa bucle infinito)
            py.mixer.music.play(loops)
            self.current_music_key = music_key
        
        except Exception as e:
            print(f"Error al cargar la musica {music_key} en {state_name}: e")

    def stop_music(self) -> None:
        """Detiene la reproduccion de la musica de fondo actual"""
        py.mixer.music.stop()
        self.current_music_key = None

    def update_music_volume(self) -> None:
        "Actualiza instantaneamente el volumen"
        volume = data.get("volume_music", 0.5)
        py.mixer.music.set_volume(volume)