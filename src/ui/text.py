import pygame as py
class Text:
    def __init__(self, position_type: str, offset_x: int, offset_y: int, message: str, color: tuple[int, int, int], font: py.font.Font, antialias: bool):
        
        #Parámetros para la posición del texto
        self.position_type = position_type
        self.offset_x = offset_x
        self.offset_y = offset_y

        #Creamos la superficie de texto y escribimos
        self.text_surface = font.render(message, antialias, color)
        #obtenemos su rect
        self.rect = self.text_surface.get_rect()
        self.is_positioned = False

    def _calculate_position(self, screen: py.Surface):
        screen_rect = screen.get_rect()

        #Puntos de anclaje con respecto a la pantalla
        if self.position_type == "center":
            self.rect.center = screen_rect.center
        elif self.position_type == "bottom_center":
            self.rect.midbottom = screen_rect.midbottom
        elif self.position_type == "top_center":
            self.rect.midtop = screen_rect.midtop
        elif self.position_type == "bottom_right":
            self.rect.bottomright = screen_rect.bottomright
        elif self.position_type == "top_left":
            self.rect.topleft = screen_rect.topleft
        
        #Ajustes de posición en píxeles
        self.rect.x += self.offset_x
        self.rect.y += self.offset_y

        #Bandera para que solo se posicione la primera vez
        self.is_positioned = True
        
    def draw(self, screen: py.Surface):
        """Dibuja el icono en su posición con la textura actual"""
        if not self.is_positioned:
            self._calculate_position(screen)

        screen.blit(self.text_surface, self.rect)