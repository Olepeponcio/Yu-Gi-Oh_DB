class WorkflowState:
    def __init__(self, action_count):
        if action_count < 1:
            raise ValueError("El flujo necesita al menos una acción.")
        self.action_count = action_count
        self.current_index = 0

    def is_enabled(self, index):
        return index == self.current_index

    def complete(self, index, succeeded):
        if index != self.current_index:
            raise ValueError("La acción completada no corresponde al paso activo.")
        if not succeeded:
            return self.current_index
        if index == self.action_count - 1:
            self.current_index = 0
        else:
            self.current_index += 1
        return self.current_index
