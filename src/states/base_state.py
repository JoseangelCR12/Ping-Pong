import pygame as py
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..resources.resource_manager import ResourceManager

class BaseState:

    def __init__(self, resource_manager: "ResourceManager") -> None:
        self.resource_manager = resource_manager
        self.next_state = None

    def enter(self, datos=None): 
        pass

    def exit(self): 
        pass

    def pause(self): 
        pass

    def resume(self): 
        pass

    def handle_input(self, events: list[py.event.Event]) -> None:
        pass
    
    def update(self, dt: float) -> None:
        pass
    
    def render(self, screen: py.Surface) -> None:
        raise NotImplementedError