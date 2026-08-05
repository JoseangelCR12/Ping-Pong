import os
from ..utils import json_helper
from ..utils.paths import get_asset_path

#AJUSTES POR DEFECTO
data = {     
    "volume_music" : 0.5,
    "volume_sfx" : 0.7,
    "wheel_sensitivity" : 15,
    "theme" : "classic",
    "camera_mode" : "standard",
    "cpu_level" : 2,

    #Ajustes del pseudo3D
    "horizon_line" : 0, #Linea del horizonte, para el dibujado en pantalla con efecto pseudo 3D
    "camera_depth" : -200, #Profundidad de la camara en el eje Y 
    "camera_height" : 304, #Altura de la camara en el eje Z, desde el lado del jugador

    "focal_length" : 456, #Distancia focal para la proyeccion pseudo 3D, mayor distancia focal significa menor escalado en la distancia
    "k_padding" : 228 #Constante para evitar division por cero en la proyeccion pseudo 3D y suavizar el escalado en la distancia
}

SETTINGS_FILE = get_asset_path("save/user_settings.json")

#FUNCIONES PARA CAMBIAR LOS AJUSTES

def set_music_volume(value: float):
    """Ajusta el volumen de la musica"""
    data["volume_music"] = max(0.0, min(1.0, value))

def set_sfx_volume(value: float):
    """Ajusta el volume de los efectos de sonido (sounds)"""
    data["volume_sfx"] = max(0.0, min(1.0, value))

def set_wheel_sensitivity(value: int):
    """Ajusta la sensibilidad de la ruedita del mouse (Movimiento en Z)"""
    data["wheel_sensitivity"] = max(2, min(20, value))

def set_cpu_level(value: int):
    """Ajusta la dificultad de la cpu"""
    data["cpu_level"] = max(0, min(3, value))

def set_theme(new_theme: str):
    """Cambia el tema visual si es valido"""
    if new_theme in ["classic", "udo", "green", "purple"]:
        data["theme"] = new_theme

def set_camera_preset(preset_name: str):
    presets = {
        "fisheye": {"horizon_line" : 90,  "camera_depth" : -550, "camera_height" : 120, "focal_length" : 200, "k_padding" : -400},
        "standard": {"horizon_line" : -15,  "camera_depth" : -180, "camera_height" : 304, "focal_length" : 456, "k_padding" : 228}
    }
    if preset_name in presets:
        data.update(presets[preset_name])
        data.update({"camera_mode" : preset_name})

# METODOS PARA PERSISTENCIA DE AJUSTES
def load_from_file():
    """Lee el json y sincroniza el diccionario de memoria"""
    if not os.path.exists(SETTINGS_FILE):
        return 
    saved_data = json_helper.read_json(SETTINGS_FILE)

    if saved_data:
        for key in data:
            if key in saved_data:
                data[key] = saved_data[key]

def save_to_file():
    """Guarda el diccionario data en el disco"""
    json_helper.write_json(SETTINGS_FILE, data)
