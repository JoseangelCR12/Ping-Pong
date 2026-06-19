import pygame as py

class Button:
    def __init__(self, position_type, offset_x, offset_y,image_normal, image_hover, image_pressed):

        self.image_normal = image_normal
        self.image_hover = image_hover
        self.image_pressed =image_pressed

        self.image = self.image_normal
        
        #Parámetros para la posición del botón
        self.position_type = position_type
        self.offset_x = offset_x
        self.offset_y = offset_y

        #El rect aún no se posiciona, no tenemos la info de screen
        self.rect = self.image.get_rect()
        self.is_positioned = False
        self.is_hovered = False

    def _calculate_position(self, screen):
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

    def handle_input(self, event):
        if not self.is_positioned:
            return False

        if event.type == py.MOUSEBUTTONDOWN and event.button == py.BUTTON_LEFT:
            if self.rect.collidepoint(event.pos):
                self.image = self.image_pressed
                return True
        return False

    def update(self, mouse_pos):
        """Actualiza el aspecto del botón de acuerdo a la posición del cursor."""
        if not self.is_positioned:
            return
        
        self.is_hovered = self.rect.collidepoint(mouse_pos)

        if self.is_hovered:
            self.image = self.image_pressed
        else:
            self.image = self.image_normal
        
    def draw(self, screen):
        """Dibuja el botón en su posición con la textura actual"""
        if not self.is_positioned:
            self._calculate_position(screen)

        screen.blit(self.image, self.rect)