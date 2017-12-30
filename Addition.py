class Addition(object):
    """description of class"""

    def __init__(self, basegate, qubits, layer, controls = None, first = None, last = None, **kwargs):
        super().__init__(**kwargs)
        self.basegate = basegate
        self.qubits = qubits
        self.layer = layer
        self.controls = controls
        self.first = first
        self.last = last


