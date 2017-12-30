class Gate(object):
    """description of class"""

    def __init__(self, gateinfo, qubits, basegate, controls = None):
        qubits = qubits if type(qubits) is list else [qubits]
        self.info = gateinfo
        self.qubits = qubits
        self.basegate = basegate
        self.controls = controls

    @property
    def last_qubit(self):
        return self.first_qubit + self.info.size - 1

    @property
    def size(self):
        return self.info.size

    @property
    def matrix(self):
        return self.info.matrix

    @property
    def signature(self):
        return str(self.info.signature)

    @property
    def offset(self):
        return self.info.offset

    @property
    def first_qubit(self):
        return self.qubits[0] + self.info.offset

    def __hash__(self):
        return hash(id(self))

    def __eq__(self, other):
        if not isinstance(other, type(self)): return TypeError("comparing objects of different classes")
        return id(self) == id(other)

    def __str__(self, **kwargs):
        return str(self.info.signature)
        
        





