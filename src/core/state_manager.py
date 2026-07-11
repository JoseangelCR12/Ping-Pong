import config

class StateManager:

    def __init__(self, states_factory):
        self._current_state = None
        self._states_stack = []
        #guardamos la funcion que crea los estados desde el game()
        self._states_factory = states_factory

    def handle_input(self, events):
        if self._current_state:
            self._current_state.handle_input(events)
            self._check_transitions(self._current_state)

    def update(self, dt):
        if self._current_state:    
            self._current_state.update(dt)

    def render(self, screen):
        screen.fill(config.BG_COLOR)
        if self._current_state:
            for state in self._states_stack:
                state.render(screen)
            self._current_state.render(screen)

    def change_state(self, new_state, datos=None):
        if self._current_state:
            self._current_state.exit()
        self._states_stack.clear()
        self._current_state = new_state
        self._current_state.enter(datos)

    def _push_state(self, new_state, datos=None):
        if self._current_state:
            self._current_state.pause()
            self._states_stack.append(self._current_state)
        self._current_state = new_state
        self._current_state.enter(datos)

    def _pop_state(self):
        if self._current_state:
            self._current_state.exit()
        if self._states_stack:
            self._current_state = self._states_stack.pop()
            self._current_state.resume()
        else:
            self._current_state = None

    def _check_transitions(self, active_state):
        if not active_state:
            return      

        #procesamos retorno (pop)
        if active_state.pop_request:
            active_state.pop_request = False
            self._pop_state()
            return
        
        destination = None
        next_type = None
        
        #Evaluacion de nuevos destinos
        if active_state.next_change_state is not None:
            destination = active_state.next_change_state
            active_state.next_change_state = None
            next_type = "change"

        elif active_state.next_push_state is not None:
            destination = active_state.next_push_state
            active_state.next_push_state = None
            next_type = "push"
            
        if destination is not None:
            #inyeccion automatizada de dependencias desde el game con el modulo routes y la funcion del game()
            new_state = self._states_factory(destination)
            if new_state is None:
                return
            
            #Elegimos el metodo correspondiente al estado siguiente
            if next_type == "change":       
                self.change_state(new_state)
            elif next_type == "push":
                self._push_state(new_state)
        
    
