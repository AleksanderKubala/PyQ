from Window import Window
from CircuitManager import CircuitManager
from Icons import Icons
from PyQt5.QtCore import Qt

class App(object):
    """description of class"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Icons.get_icon()
        self.init_circuit()
        self.init_window()
        self.bind_events()
        self.window.show()

    def init_circuit(self):
        self.circuit_manager = CircuitManager()

    def init_window(self):
        self.window = Window()

    def bind_events(self):
    
        self.window.basegate.gateChanged.connect(self.window.circuit.on_gateChanged)
        self.window.register.registerChanged.connect(self.circuit_manager.on_register_change)
        self.window.actions.computeCircuit.connect(self.circuit_manager.on_compute)
        self.window.actions.qubitCountChange.connect(self.window.register.on_qubitCountChange)
        self.window.register.registerResized.connect(self.circuit_manager.on_register_resized)
        self.window.circuit.removalRequested.connect(self.circuit_manager.on_removal_request)
        self.window.circuit.additionRequested.connect(self.circuit_manager.on_addition_request)
        self.circuit_manager.circuitChanged.connect(self.window.circuit.on_circuit_change)
        self.circuit_manager.circuitResized.connect(self.window.circuit.on_circuitResized)
        self.circuit_manager.resultsRetrieved.connect(self.window.results.on_resultsRetrieved)
        


