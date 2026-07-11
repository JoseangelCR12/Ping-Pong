from typing import Any

class CacheManager:
    def __init__(self):
        #Guarda referencias directa tanto a surfaces como a listas de surfaces para spritestacking o sonidos
        self._cache_storage: dict[str, Any] = {}
    
    def get(self, key: str) -> Any:
        """Devuelve la referencia guardada, de no existir retorna None"""
        return self._cache_storage.get(key, None)
    
    def save(self, key: str, data: Any) -> None:
        """Guarda la referencia del objeto en el diccionario de cache"""
        self._cache_storage[key] = data

    def clear_all(self) -> None:
        """Borra toda la cache, util al salir de un estado"""
        self._cache_storage.clear()