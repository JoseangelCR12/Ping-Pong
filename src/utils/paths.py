from pathlib import Path

BASE_DIR = Path(__file__).absolute().parent.parent.parent

def get_asset_path(relative_path: str) -> str:
    """ convierte una ruta fija a una ruta que sirva en cualquier os """
    if not relative_path:
        return ""
    
    #dividimos las carpetas y direcciones con la barra oblicua del diccionario de assets
    clean_path = relative_path.replace("\\", "/")
    parts = clean_path.split("/")

    #se unen las partes a partir de la raiz del proyecto
    #El asterisco desempaqueta la lista de argumentos(las carpetas por las que se llega al asset)
    return str(BASE_DIR.joinpath(*parts))
