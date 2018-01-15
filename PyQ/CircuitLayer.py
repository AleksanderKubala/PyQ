import numpy
import sympy
import random
from PyQ.Gate import Gate
from PyQ.GateInfoRegister import GateInfoRegister
from PyQ.Gatename import Gatename
from PyQ.MeasurementResult import MeasurementResult


class CircuitLayer(object):
    """description of class"""

    identity = GateInfoRegister.instance().register[Gatename.IDENTITY]

    def __init__(self, register_size):
        self.is_identity = True
        self.gates = [Gate(CircuitLayer.identity, i, str(CircuitLayer.identity.signature)) for i in range(register_size)]
        self.measurement_slots = []
        self.update()

    def add_gate(self, gate):
        cleaning = self.clean_range(gate.first_qubit, gate.last_qubit)
        for i in range(gate.first_qubit, gate.last_qubit + 1):
            self.gates[i] = gate
            if gate.is_measurement:
                self.measurement_slots.append(gate.first_qubit)
        self.update()
        return cleaning

    def clean_range(self, begin = 0, end = None):
        gate_list = self.get_gates(begin, end)
        return self._remove_gates(gate_list)

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
        self.update()
        return cleaning

    def update(self):
        self.measurement_slots.sort()
        self._add_identities()
        if self.has_measurements() is False:
            self._calculate_transformation()
            self.is_identity = self._check_identity()

    def get_gates(self, begin = 0, end = None):
        gate_list = set()
        if end is None or end >= len(self.gates): end = len(self.gates) - 1
        if begin < 0: begin = 0
        if begin >= len(self.gates): begin = len(self.gates) - 1
        for i in range(begin, end + 1):
            if self.gates[i] is not None:
                gate_list.add(self.gates[i])
        return list(gate_list)

    def has_measurements(self):
        if len(self.measurement_slots) > 0:
            return True
        else:
            return False

    def measure(self, register):
        measurements = self._calculate_measurements(register)
        probabilities = [numpy.dot(register.transpose(), measurement[1]) for measurement in measurements]
        bound = 0
        roll = random.uniform(0, 1)
        for i in range(0, len(probabilities)):
            bound = bound + probabilities[i]
            if roll <= bound:
                state = (measurements[i])[1]/sympy.sqrt(probabilities[i])
                return MeasurementResult(state, self.measurement_slots, (measurements[i])[0])

    def _calculate_measurements(self, register):
        measurements = []
        shift = 0
        measurement_count = len(self.measurement_slots)
        for i in range(2**measurement_count):
            bit_value = ''
            for j in range(measurement_count - 1, -1, -1):
                projection = i & (1 << (measurement_count - 1 - j))
                self.gates[self.measurement_slots[j]].set_transformation(projection)
                bit_value = str(projection) + bit_value
            self._calculate_transformation()
            measurements.append((bit_value, numpy.dot(self.transformation, register)))
        return measurements

    def _calculate_transformation(self):
        gate_list = []
        last_gate = None
        for gate in self.gates:
            if gate is not last_gate:
                gate_list.append(gate)
                last_gate = gate
        self.transformation = gate_list[0].transformation
        gate_list.pop(0)
        for gate in gate_list:
            self.transformation = numpy.kron(self.transformation, gate.transformation)

    def _check_identity(self):
        return (self.transformation == numpy.identity(self.transformation.shape[0])).all()
                
    def _remove_gates(self, gate_list):
        indices_list = list()
        if gate_list:
            for gate in gate_list:
                for i in range(gate.first_qubit, gate.last_qubit + 1):
                    indices_list.append(i)
            for index in indices_list:
                if self.gates[index].is_measurement:
                    self.measurement_slots.remove(self.gates[index].first_qubit)
                self.gates[index] = None
        self.update()
        return indices_list

    def _add_identities(self):
        for i in range(len(self.gates)):
            if self.gates[i] is None:
                self.gates[i] = Gate(CircuitLayer.identity, i, str(CircuitLayer.identity.signature))

