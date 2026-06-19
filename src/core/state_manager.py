class StateManager:

    def __init__(self):
        self.current_state = None
        self._states_stack = []

    def change_state(self, new_state, datos=None):
        if self.current_state:
            self.current_state.exit()
        self.current_state = new_state
        self.current_state.enter(datos)

    def push_state(self, new_state, datos=None):
        if self.current_state:
            self.current_state.pause()
            self._states_stack.append(self.current_state)
        self.current_state = new_state
        self.current_state.enter(datos)

    def pop_state(self):
        if self.current_state:
            self.current_state.exit()
        if self._states_stack:
            self.current_state = self._states_stack.pop()
            self.current_state.resume()
        else:
            self.current_state = None
    
