import pygame as py

class Renderer:
    def __init__(self, screen):
        self.screen = screen

    def render_sprite_stack(self, sprite_slices, screen_x, screen_y, scale):
        base_width = sprite_slices[0].get_width()
        base_height = sprite_slices[0].get_height()

        for i, slice_surface in enumerate(sprite_slices):
            # Escala de acuerdo a la profundidad
            new_w = max(1, int(base_width * scale))
            new_h = max(1, int(base_height * scale))
            scaled_slice = py.transform.scale(slice_surface, (new_w, new_h)) 

            #vamos ajustando el desfase en Y (originalmente 1) que permite el efecto 3d de acuerdo a la profundidad (porque los objetos se hacen mas pequeños)
            layer_offset_y = int(i * 1 * scale)
            current_sy = screen_y - layer_offset_y

            #Blint en la pantalla
            self.screen.blit(scaled_slice, (screen_x, current_sy))