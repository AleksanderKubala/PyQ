from GridFrame import GridFrame
from PyQt5.QtWidgets import QPushButton, QLineEdit
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import pyqtSignal
import config

class ActionFrame(GridFrame):
    """description of class"""

    computeCircuit = pyqtSignal(int)
    qubitCountChange = pyqtSignal(int)

    def __init__(self, rows = 0, cols = 0, spacing = None, margins = None, **kwargs):
        super().__init__(rows, cols, spacing, margins, **kwargs)
        self.compute = QPushButton("Compute")
        self.compute.released.connect(self.on_compute_release)
        self.grid.addWidget(self.compute, 0, 0, 2, 2)

        self.compute_to = QPushButton("Compute To")
        self.compute_to.released.connect(self.on_compute_to_release)
        self.grid.addWidget(self.compute_to, 2, 0, 2, 2)

        self.step = QLineEdit(str(config.INITIAL_LAYERS_COUNT))
        validator = QIntValidator(1, config.INITIAL_LAYERS_COUNT, self.step)
        self.step.setValidator(validator)
        self.step.editingFinished.connect(self.on_step_changed)
        self.grid.addWidget(self.step, 2, 2, 2, 2)

        self.qubits = QPushButton("Resize Register")
        self.qubits.released.connect(self.on_qubits_change)
        self.grid.addWidget(self.qubits, 0, 4, 2, 2)

        self.qubits_count = QLineEdit(str(config.INITIAL_QUBITS))
        validator = QIntValidator(1, config.SIZE_RESTRICTION, self.qubits_count)
        self.qubits_count.setValidator(validator)
        self.qubits_count.editingFinished.connect(self.on_qubits_count_changed)
        self.grid.addWidget(self.qubits_count, 0, 6, 2, 2)

    def on_compute_release(self):
        self.computeCircuit.emit(0)

    def on_compute_to_release(self):
        self.computeCircuit.emit(int(self.step.text()))

    def on_step_changed(self):
        result = self.step.validator().validate(self.step.text(), 0)
        if result[0] != QIntValidator.Acceptable:
            self.step.setText(str(config.INITIAL_LAYERS_COUNT))

    def on_qubits_change(self):
        self.qubitCountChange.emit(int(self.qubits_count.text()))

    def on_qubits_count_changed(self):
        result = self.step.validator().validate(self.step.text(), 0)
        if result[0] != QIntValidator.Acceptable:
            self.step.setText(str(config.INITIAL_QUBITS))


        
