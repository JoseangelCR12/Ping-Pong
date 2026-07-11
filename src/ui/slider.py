import pygame as py
from .button import Button

class Slider(Button):
    def __init__(self, position_type: str, offset_x: int, offset_y: int,
                min_value: float, max_value: float, init_value: float,
                image_empty: py.Surface, #Imagen de la barra vacia
                image_full: py.Surface, #Imagen de la barra llena
                image_btn: py.Surface,  #Imagen del boton deslizante
                image_btn_h: py.Surface): #Imagen del boton deslizante cuando el raton esta encima
        
        #inicalizamos la clase base boton para que maneje el boton deslizante
        #El boton indicador es una instancia de la clase Button inicialmente ubicado en un lugar cualquiera, despues se acomoda
        super().__init__("top_left", 0, 0, image_btn, image_btn_h)
        
        #Parámetros para la posición de la barra de fondo
        self.bar_position_type = position_type
        self.bar_offset_x = offset_x
        self.bar_offset_y = offset_y
        self.bar_is_positioned = False

        #Rangos de valores genericos
        self.min = min_value
        self.max = max_value
        self.value = max(self.min, min(self.max, init_value))

        
        #Assets de las barras
        self.image_empty = image_empty
        self.image_full = image_full
        self.bar_rect = self.image.get_rect() #creamos el rect base usando las dimensiones de la barra de fondo
        
        self.sliding = False
    
    def _calculate_bar_position(self, screen: py.Surface):
        screen_rect = screen.get_rect()

        #Puntos de anclaje con respecto a la pantalla
        if self.bar_position_type == "center":
            self.bar_rect.center = screen_rect.center
        elif self.bar_position_type == "bottom_center":
            self.bar_rect.midbottom = screen_rect.midbottom
        elif self.bar_position_type == "top_center":
            self.bar_rect.midtop = screen_rect.midtop
        elif self.bar_position_type == "bottom_right":
            self.bar_rect.bottomright = screen_rect.bottomright
        elif self.bar_position_type == "top_left":
            self.bar_rect.topleft = screen_rect.topleft
        
        #Ajustes de posición en píxeles
        self.bar_rect.x += self.bar_offset_x
        self.bar_rect.y += self.bar_offset_y

        #Actualizamos la posicion del botor inicador de la clase padre
        self.is_positioned = True #Para que no se desubique despues 
        self._update_btn_pos()

        #Bandera para que solo se posicione la primera vez
        self.bar_is_positioned = True

    def _update_btn_pos(self):
        #Desplaza el boton a lo largo de la barra segun el valor
        percentage = (self.value - self.min) / (self.max - self.min)

        #Se calcula la x central del boton deslizante
        center_x = self.bar_rect.left + int(percentage * self.bar_rect.width)
        #Se centra verticalmente
        center_y = self.bar_rect.centery

        #Sincroniza el rect de colision del boton
        self.rect.center = (center_x, center_y)

    def handle_input(self, event: py.event.Event): 
        if not self.bar_is_positioned:
            return False
        
        change_value = False

        #Activar arrastre si mantienes presionado click sobre el boton
        if event.type == py.MOUSEBUTTONDOWN and event.button == py.BUTTON_LEFT:
            if self.is_hovered:
                self.sliding = True
        elif event.type == py.MOUSEBUTTONUP and event.button == py.BUTTON_LEFT:
            if self.sliding:
                self.sliding = False
                change_value = True
                
        return change_value

    def update(self, mouse_pos):
        """Actualiza el aspecto del botón deslizante de acuerdo a la posición del cursor."""
        if not self.bar_is_positioned:
            return
        
        #Actualiza self.is_hovered del boton
        super().update(mouse_pos)

        #Logica de deslizamiento
        
        if self.sliding:
            #Forzamos al del mouse a no salirse de los limites de la barra
            mouse_x = max(self.bar_rect.x, min(mouse_pos[0], self.bar_rect.x + self.bar_rect.width))
            new_percentage = (mouse_x - self.bar_rect.x) / self.bar_rect.width  
            new_value = self.min + new_percentage * (self.max - self.min)  

            if new_value != self.value:
                self.value = new_value
                self._update_btn_pos()
    
            #retenemos la textura hover mientras arrastramos el boton
            self.is_hovered = True
            self.image = self.image_hover
            

    def draw(self, screen: py.Surface):
        """Dibuja el botón en su posición con la textura actual"""
        if not self.bar_is_positioned:
            self._calculate_bar_position(screen)

        #Barra de fondo anclada
        screen.blit(self.image_empty, self.bar_rect)

        #Barra de relleno
        percentage = (self.value - self.min) / (self.max - self.min)
        fill_width = int(percentage * self.bar_rect.width)

        if fill_width > 0:
            visible_area = py.Rect(0, 0, fill_width, self.bar_rect.height)
            screen.blit(self.image_full, self.bar_rect, visible_area)
        
        #El boton deslizante
        super().draw(screen)

