import numpy
from PyQ.Gate import Gate
from PyQ.GateInfoRegister import GateInfoRegister
from PyQ.Gatename import Gatename


class CircuitLayer(object):
    """description of class"""

    identity = GateInfoRegister.instance().register[Gatename.IDENTITY]

    def __init__(self, register_size):
        self.outdated = False
        self.is_identity = True
        self.gates = [Gate(CircuitLayer.identity, i, str(CircuitLayer.identity.signature)) for i in range(register_size)]
        self.update()

    def add_gate(self, gate):
        cleaning = self.clean_range(gate.first_qubit, gate.last_qubit)
        for i in range(gate.first_qubit, gate.last_qubit + 1):
            self.gates[i] = gate
        self._add_identities()
        self.outdated = True
        return cleaning

    def clean_range(self, begin = 0, end = None):
        gate_list = set()
        if end is None: end = len(self.gates)
        if(begin < 0): begin = 0
        if(begin >= len(self.gates)): begin = len(self.gates) - 1
        for i in range(begin, end + 1):
            if self.gates[i] is not None:
                gate_list.add(self.gates[i])
        return self._remove_gates(list(gate_list))

    def clean_slots(self, slot_list):
        gate_list = set()
        for slot in slot_list:
            if self.gates[slot] is not None:
                gate_list.add(self.gates[slot])
        return self._remove_gates(list(gate_list))

    def resize(self, new_size):
        cleaning = []
        current_size = len(self.gates)
        if new_size > current_size:
            for i in range (current_size, new_size):
                self.gates.append(None)
        elif new_size < current_size:
            cleaning = self.clean_slots(tuple(i for i in range(new_size, current_size)))
            for i in range(new_size, current_size):
                self.gates.pop()
        return cleaning

    def update(self):
        self._add_identities()
        self._calculate_transformation()
        self.is_identity = self._check_identity()

    def _calculate_transformation(self):
        gate_list = []
        last_gate = None
        for gate in self.gates:
            if (gate is not last_gate):
                gate_list.append(gate)
                last_gate = gate
        self.matrix = gate_list[0].matrix
        gate_list.pop(0)
        for gate in gate_list:
            self.matrix = numpy.kron(self.matrix, gate.matrix)
        self.outdated = False

    def _check_identity(self):
        return (self.matrix == numpy.identity(self.matrix.shape[0])).all()
                
    def _remove_gates(self, gate_list):
        indices_list = list()
        if gate_list:
            for gate in gate_list:
                for i in range(gate.first_qubit, gate.last_qubit + 1):
                    indices_list.append(i)
            for index in indices_list:
                self.gates[index] = None
        self.outdated = True
        return indices_list

    def _add_identities(self):
        for i in range(len(self.gates)):
            if self.gates[i] is None:
                self.gates[i] = Gate(CircuitLayer.identity, i, str(CircuitLayer.identity.signature))

    def __str__(self, **kwargs):
        string = ""
        slot_number = 0
        last_gate = None
        for gate in self.gates:
            if gate is None:
                string = string + "Empty\n"
            else:
                if gate is last_gate:
                    string = string + ".\n"
                else:
                    string = string + str(gate) + "\n"
        return string
