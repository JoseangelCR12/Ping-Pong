import pygame as py

class CacheManager:
    # Este gestor de caché almacena sprites cortados y rotados para un acceso rápido
    def __init__(self):
        self._sprite_cache = {} #Privado porque se utiliza "_" para indicar que no debe ser accedido directamente desde fuera de la clase
        self.tamanos = {} #Almacena el tamaño de cada sprite para referencia rápida
        self.nro_slices = {} #tambien referencia rápida
    # Carga spritesheets cortados en la caché
    def cargar_spritesheets(self, spritesheets):
        for clave, (ruta, tamano, flag_angulos) in spritesheets.items():
            self.tamanos[clave] = tamano[0]
            if isinstance(flag_angulos, int) and flag_angulos > 0:
                self.cortar_vuelta(clave, ruta, tamano, flag_angulos)
            elif isinstance(flag_angulos, tuple):
                self.cortar_a_pedido(clave, ruta, tamano, flag_angulos)
            else: continue  # formato inesperado

    def cortar_vuelta(self, clave, ruta, tamano, angulo_aumento):
        if ruta in self._sprite_cache:
            return self._sprite_cache[ruta]
        
        spritesheet = py.image.load(ruta).convert_alpha()
        nro_slices = spritesheet.get_width() // tamano[0]
        self.nro_slices[clave] = nro_slices
        sprite = []
        # Cortamos el spritesheet en partes iguales según el tamaño especificado
        for i in range(nro_slices):
            slice = spritesheet.subsurface((i * tamano[0], 0) + tamano)
            sprite.append(slice)
        
        # Pre-rotamos cada sprite y los almacenamos en un diccionario
        self._sprite_cache[ruta] = {}
        for angulo in range(0, 360, angulo_aumento):
            rotada = [py.transform.rotate(s, angulo) for s in sprite]
            self._sprite_cache[ruta][angulo] = rotada
        return self._sprite_cache[ruta]

    def cortar_a_pedido(self, clave, ruta, tamano, angulos):
        if ruta in self._sprite_cache:
            return self._sprite_cache[ruta]
        
        spritesheet = py.image.load(ruta).convert_alpha()
        nro_slices = spritesheet.get_width() // tamano[0]
        self.nro_slices[clave] = nro_slices
        sprite = []
        for i in range(nro_slices):
            slice = spritesheet.subsurface((i * tamano[0], 0) + tamano)
            sprite.append(slice)
        
        self._sprite_cache[ruta] = {}
        for angulo in angulos:
            rotada = [py.transform.rotate(s, angulo) for s in sprite]
            self._sprite_cache[ruta][angulo] = rotada
        return self._sprite_cache[ruta]
    
    # Método para obtener sprites de la caché
    def obtener_sprites(self, ruta, angulo = None):
        if angulo is not None:
            return self._sprite_cache.get(ruta, {}).get(angulo)
        return self._sprite_cache.get(ruta)
