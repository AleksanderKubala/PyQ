from PyQ.Circuit import Circuit
from PyQt5.QtCore import pyqtSignal, QObject
from Addition import Addition 

class CircuitManager(QObject):
    """description of class"""

    circuitChanged = pyqtSignal(object)
    circuitResized = pyqtSignal(int)
    circuitChangeFailed = pyqtSignal(str, object)
    resultsRetrieved = pyqtSignal(object)
    simulationStarted = pyqtSignal()
    simulationUpdated = pyqtSignal(object, int, int)
    simulationStopped = pyqtSignal()

    def __init__(self, **kwargs):
        super().__init__(**kwargs) 
        self.circuit = Circuit()

    def on_run_simulation(self, time):
        self.simulationStarted.emit()
        self.circuit.start(time)
        self.simulationUpdated.emit(self.circuit.running, self.circuit.next_step - 1, self.circuit.layer_count)
        results = self.circuit.get_results()
        self.resultsRetrieved.emit(results)
        if not self.circuit.running:
            self.simulationStopped.emit()

    def on_next_step(self):
        self.circuit.next()
        self.simulationUpdated.emit(self.circuit.running, self.circuit.next_step - 1, self.circuit.layer_count)
        results = self.circuit.get_results()
        self.resultsRetrieved.emit(results)
        if not self.circuit.running:
            self.simulationStopped.emit()

    def on_stop_simulation(self):
        self.circuit.stop()
        self.simulationStopped.emit()

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
        




