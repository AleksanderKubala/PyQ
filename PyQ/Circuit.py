import numpy
from PyQ.CircuitLayer import CircuitLayer
from PyQ.GateRequest import GateRequest
from PyQ.GateInfoRegister import GateInfoRegister
from PyQ.CircuitChanges import CircuitChanges
from PyQ.ComputeResult import ComputeResult
from PyQ.Gatename import Gatename
from PyQ.DisturbanceGenerator import DisturbanceGenerator, RandomValueGenerator
from sympy import *
import PyQ.config as cfg

class Circuit(object):
    """description of class"""

    size_restriction = cfg.SIZE_RESTRICTION
    default_size = cfg.DEFAULT_SIZE

    def __init__(self, register_size:int = cfg.DEFAULT_SIZE, layer_count:int = cfg.DEFAULT_LAYER_COUNT):
        if register_size < 1:
            register_size = cfg.DEFAULT_SIZE
        if register_size > cfg.SIZE_RESTRICTION:
            register_size = cfg.SIZE_RESTRICTION
        if layer_count < 1:
            layer_count = cfg.DEFAULT_LAYER_COUNT
        if layer_count > cfg.LAYER_RESTRICTION:
            layer_count = cfg.LAYER_RESTRICTION
        matrix_size = 2**register_size
        self.layer_count = layer_count
        self.size = register_size
        self.register = numpy.matrix(numpy.zeros(shape = (matrix_size, 1)))
        self.register[0] = 1
        self.current_state = 0
        self.layers = [CircuitLayer(register_size) for i in range(self.layer_count)]
        self.transformation = numpy.matrix(numpy.identity(matrix_size))
        self.result = self.register.copy()
        self.next_step = 1
        self.running = False
        self.measured = ['?']*self.size
        self.ideal = True
        self.disturbance_probability = self.set_disturbance_probability(cfg.DISTURBANCE_PROBABILITY)

    def add(self, gate, qubits, layer, controls = None):
        qubits, layer = self._check_requested_params(qubits, layer)
        size = max(qubits) - min(qubits) + 1
        request = GateRequest(gate, min(qubits), size, controls)
        gate = GateInfoRegister.instance().get(request)
        changes = CircuitChanges()
        if gate is not None: 
            if gate.first_qubit < 0: raise ValueError("This gate cannot be set on given qubit: {0}.".format(qubits))
            changes.add_removed(layer, self.layers[layer].add_gate(gate))
            changes.add_added(layer, gate)
            if gate.basegate == Gatename.MEASUREMENT:
                for i in range(layer + 1, self.layer_count):
                    changes.add_removed(i, self.layers[i].clean_slots((gate.first_qubit,)))
        return changes

    def remove(self, qubits, layer):
        qubits, layer = self._check_requested_params(qubits, layer)
        changes = CircuitChanges()
        changes.add_removed(layer, self.layers[layer].clean_slots(qubits))
        return changes

    def next(self):
        if self.running is False:
            self.start(1)
        else:
            layer = self.layers[self.next_step - 1]
            if not layer.is_identity:
                self.result = numpy.dot(layer.transformation, self.result)
            if not self.ideal:
                if RandomValueGenerator.binary_distribution(cfg.DISTURBANCE_PROBABILITY):
                    disturbance = DisturbanceGenerator.create_disturbance(self.size)
                    self.result = numpy.dot(disturbance, self.result)
            if layer.has_measurements():
                measurement = layer.measure(self.result)
                self.result = measurement.state
                for i in range(len(measurement.bit_number)):
                    self.measured[measurement.bit_number[i]] = measurement.value[i]
            self.next_step += 1
            if self.next_step > self.layer_count:
                self.stop()
            simplify(self.result)

    def start(self, time = 0):
        self.running = True
        if (time <= 0) or (time > self.layer_count): time = self.layer_count
        self.result = self.register.copy()
        self.next_step = 1
        self.measured = ['?']*self.size
        while (self.next_step <= time) and (self.next_step <= self.layer_count):
            self.next()

    def stop(self):
        self.running = False

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
            self.measured = ['?']*self.size
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
                single_result = "{0:b}".format(i)
                single_result = "0"*(self.size - len(single_result)) + single_result
                results.append(ComputeResult(nsimplify(amplitude), single_result, round((numpy.absolute(N(amplitude,6))**2)*100, 5)))
        return results

    def set_ideal(self, ideal, probability=cfg.DISTURBANCE_PROBABILITY):
        if not ideal:
            self.set_disturbance_probability(probability)
            self.ideal = False
        else:
            self.ideal = True

    def set_disturbance_probability(self, probability):
        if probability < 0 or probability > 1:
            raise ValueError("Probability value out of range (0, 1)")
        else:
            self.disturbance_probability = probability

    def _clear_register(self, value = 0):
        for i in range(2**self.size):
            self.register[i] = value

    def _check_requested_params(self, qubits, layer):
        qubits = [qubits] if type(qubits) is int else qubits
        layer = [layer] if type(layer) is int else layer
        first = min(qubits)
        last = max(qubits)
        if first < 0 or last >= self.size: raise ValueError("invalid qubit number: {0}".format(qubits))
        if layer[0] < 0 or layer[0] >= self.layer_count: raise ValueError("invalid layer number: {0}".format(layer[0]))
        return qubits, layer[0]

        
       



        


        


