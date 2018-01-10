class GateRequest(object):
    
    def __init__(self, gate, qubit, size = 1, controls = None):
        self.gate = gate
        self.qubit = qubit
        self._size(size)
        self._controls(controls)

    @property
    def basegate(self):
        return self.gate + str(self.size) if self.size > 1 else self.gate

    def _size(self, size):
        if size < 2: self.size = 1
        else: self.size = size

    def _controls(self, controls):
        control_list = [[], []]
        if controls is not None:
            controls = [controls] if type(controls) is int else controls 
            for value in controls:
                if value - self.qubit < 0: control_list[0].append(value - self.qubit)
                if value - (self.qubit + self.size - 1) > 0: control_list[1].append(value - (self.qubit + self.size - 1))
        self.controls = control_list





