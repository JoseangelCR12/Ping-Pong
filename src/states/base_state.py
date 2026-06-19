import pygame as py

class BaseState:

    def __init__(self, resource_manager) -> None:
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
        raise NotImplementedError
    
    def update(self, dt: float) -> None:
        raise NotImplementedError
    
    def render(self, screen: py.Surface) -> None:
        raise NotImplementedError