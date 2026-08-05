import pygame as py
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..resources.resource_manager import ResourceManager

class BaseState:

    def __init__(self, resource_manager: "ResourceManager") -> None:
        self.resource_manager = resource_manager
        #Flags de transicion
        self.next_change_state = None #Para cambiar completamente de estado
        self.next_push_state = None #Para un overlay como el menu de opciones, la pusa, etc.

        #Flag booleano para retroceder en la pila de estados
        self.pop_request = False

    def enter(self): 
        pass

    def exit(self): 
        pass

    def pause(self):
        pass

    def resume(self):
        pass

    def handle_input(self, events: list[py.event.Event]) -> None:
        raise NotImplementedError
    
    def update(self, dt: float) -> None:
        raise NotImplementedError
    
    def render(self, screen: py.Surface) -> None:
        raise NotImplementedError