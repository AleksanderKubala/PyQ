import numpy
from PyQ.CircuitLayer import CircuitLayer
from PyQ.GateRequest import GateRequest
from PyQ.GateInfoRegister import GateInfoRegister
from PyQ.CircuitChanges import CircuitChanges
from PyQ.ComputeResult import ComputeResult
from sympy import *
import PyQ.configuration as cfg

class Circuit(object):
    """description of class"""

    size_restriction = cfg.SIZE_RESTRICTION
    default_size = cfg.DEFAULT_SIZE

    def __init__(self, register_size:int = cfg.DEFAULT_SIZE, layer_count:int = cfg.DEFAULT_LAYER_COUNT):
        matrix_size = 2**register_size
        self.layer_count = layer_count
        self.size = register_size
        self.register = numpy.matrix(numpy.zeros(shape = (matrix_size, 1)))
        self.register[0] = 1
        self.current_state = 0
        self.layers = [CircuitLayer(register_size) for i in range(self.layer_count)]
        self.transformation = numpy.matrix(numpy.identity(matrix_size))
        self.result = self.register.copy()

    def add(self, gate, qubits, layer, controls = None):
        qubits = self._check_requested_params(qubits, layer)
        size = max(qubits) - min(qubits) + 1
        request = GateRequest(gate, min(qubits), size, controls)
        gate = GateInfoRegister.instance().get(request)
        changes = CircuitChanges()
        if gate is not None: 
            if gate.first_qubit < 0: raise ValueError("This gate cannot be set on given qubit: {0}.".format(qubits))
            changes.add_removed(layer, self.layers[layer].add_gate(gate))
            changes.add_added(layer, gate)
        return changes

    def remove(self, qubits, layer):
        qubits = self._check_requested_params(qubits, layer)
        changes = CircuitChanges()
        changes.add_removed(layer, self.layers[layer].clean_slots(qubits))
        return changes
        
    def compute(self, time = 0):
        if (time <= 0) or (time > self.layer_count): time = self.layer_count
        self._update_layers()
        matrix = numpy.matrix(numpy.identity(2**self.size))
        for i in range(time - 1, -1, -1):
            if not self.layers[i].is_identity:
                matrix = numpy.matrix(numpy.dot(matrix, self.layers[i].matrix))
        self.transformation = matrix
        self.result = numpy.dot(self.transformation, self.register)
        return self.get_results()

    def resize(self, new_size):
        changes = CircuitChanges()
        if(new_size != self.size):
            if (new_size <= 0) or (new_size > Circuit.size_restriction):
                raise ValueError("register size must be in range: (0, {0})".format(Circuit.size_restriction))
            if new_size < self.size:
                self.set_register(self.current_state >> (self.size - new_size))
                self.register.resize((2**new_size, 1), refcheck = False)
            else:
                self.register.resize((2**new_size, 1), refcheck = False)
                self.set_register(self.current_state << (new_size - self.size))
            self.size = new_size
            for i in range(len(self.layers)):
                changes.add_removed(i, self.layers[i].resize(new_size))
        return changes

    def set_register(self, value):
        self._clear_register()
        self.register[value] = 1
        self.current_state = value

    def set_zeros(self):
        self._clear_register()
        self.register[0] = 1
        self.current_state = 0

    def set_ones(self):
        self._clear_register()
        self.register[-1] = 1
        self.current_state = self.register.shape[0] - 1

    def get_results(self):
        results = list()
        for i in range(2**self.size):
            if self.result.item(i) != 0:
                amplitude = self.result.item(i)
                # if type(amplitude) is complex: amplitude = complex(round(amplitude.real, 4), round(amplitude.imag, 4))
                # else: amplitude = complex(round(amplitude, 4))
                single_result = "{0:b}".format(i)
                single_result = "0"*(self.size - len(single_result)) + single_result
                results.append(ComputeResult(nsimplify(amplitude), single_result, round((numpy.absolute(self.result.item(i))**2)*100, 3)))
        return results

    def get_computed_register(self):
        return self.result

    def _update_layers(self):
        for layer in self.layers:
            if layer.outdated:
                layer.update()

    def _clear_register(self, value = 0):
        for i in range(2**self.size):
            self.register[i] = value

    def _check_requested_params(self, qubits, layer):
        qubits = [qubits] if type(qubits) is int else qubits
        first = min(qubits)
        last = max(qubits)
        if first < 0 or last >= self.size: raise ValueError("invalid qubit number: {0}".format(qubits))
        if layer < 0 or layer >= self.layer_count: raise ValueError("invalid layer number: {0}".format(layer))
        return qubits

        
       



        


        


