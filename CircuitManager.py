from PyQ.Circuit import Circuit
from PyQt5.QtCore import pyqtSignal, QObject
from Addition import Addition 

class CircuitManager(QObject):
    """description of class"""

    circuitChanged = pyqtSignal(object)
    circuitResized = pyqtSignal(int)
    circuitChangeFailed = pyqtSignal(str, object)
    resultsRetrieved = pyqtSignal(object)

    def __init__(self, **kwargs):
        super().__init__(**kwargs) 
        self.prepare_circuit()
        

    def prepare_circuit(self):
        self.circuit = Circuit()
        self.circuit.compute()

    def on_compute(self, step):
        results = self.circuit.compute(step)
        self.resultsRetrieved.emit(results)

    def on_register_change(self, value):
        self.circuit.set_register(value)

    def on_removal_request(self, qubit, layer):
        result = self.circuit.remove(qubit, layer)
        self.circuitChanged.emit(result)

    def on_addition_request(self, request):
        result = self.circuit.add(request.basegate, request.qubits, request.layer, request.controls)
        for i in range(len(result.added)):
            addition = (result.added[i])[1]
            result.added[i] = (result.added[i][0], Addition(addition.basegate, addition.qubits, request.layer, addition.controls, addition.first_qubit, addition.last_qubit))
        self.circuitChanged.emit(result)

    def on_register_resized(self, new_size):
        results = self.circuit.resize(new_size)
        self.circuitChanged.emit(results)
        self.circuitResized.emit(new_size)
        




