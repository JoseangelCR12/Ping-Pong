import json
import os
from typing import Any, Dict

def read_json(file_path: str) -> Dict[str, Any]:
    """Lee un archivo JSON de forma segura"""   
    if not os.path.exists(file_path):
        return {}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"No se pudo leer el archivo en {file_path}: {e}")
        return {}
    
def write_json(file_path: str, data: Dict[str, Any]) -> bool:
    """Escribe los datos en un archivo JSON asegurando que el directorio exista"""
    try: 
        #Extrae de forma segura la ruta desde la carptea contenedora
        dir_name = os.path.dirname(file_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
            return True
    except IOError as e:
        print(f"No se pudo escribir el archivo en {file_path}: {e}")
        return False