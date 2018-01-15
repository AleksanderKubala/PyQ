from GridFrame import GridFrame
from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import pyqtSignal
import config

class ActionFrame(GridFrame):
    """description of class"""

    runSimulation = pyqtSignal(int)
    nextStep = pyqtSignal()
    stopSimulation = pyqtSignal()
    qubitCountChange = pyqtSignal(int)

    def __init__(self, rows = 0, cols = 0, spacing = None, margins = None, **kwargs):
        super().__init__(rows, cols, spacing, margins, **kwargs)
        self.simulation_status = '-'
        self.current_step = '-'
        self.total_steps = '-'

        self.run = QPushButton("Run Simulation")
        self.run.released.connect(self.on_run_release)
        self.grid.addWidget(self.run, 0, 0, 1, 1)

        self.manual = QPushButton("Run Manually From")
        self.manual.released.connect(self.on_manual_release)
        self.grid.addWidget(self.manual, 1, 0, 1, 1)

        self.start_step = QLineEdit(str(config.INITIAL_LAYERS_COUNT))
        validator = QIntValidator(1, config.INITIAL_LAYERS_COUNT, self.start_step)
        self.start_step.setValidator(validator)
        self.start_step.editingFinished.connect(self.on_step_changed)
        self.grid.addWidget(self.start_step, 1, 1, 1, 1)

        self.next = QPushButton("Next")
        self.next.released.connect(self.on_next_release)
        self.grid.addWidget(self.next, 2, 0, 1, 1)

        self.stop = QPushButton("Stop")
        self.stop.released.connect(self.on_stop_release)
        self.grid.addWidget(self.stop, 2, 1, 1, 1)

        self.status = QLabel("Status: " + self.simulation_status)
        self.grid.addWidget(self.status, 3, 0, 1, 1,)

        self.step = QLabel("Step: " + self.current_step)
        self.grid.addWidget(self.step, 4, 0, 1, 1)

        self.total = QLabel("Total: " + self.total_steps)
        self.grid.addWidget(self.total, 4, 1, 1, 1)

        self.resize = QPushButton("Resize Register")
        self.resize.released.connect(self.on_resize_release)
        self.grid.addWidget(self.resize, 0, 2, 1, 1)

        self.qubits_count = QLineEdit(str(config.INITIAL_QUBITS))
        validator = QIntValidator(1, config.SIZE_RESTRICTION, self.qubits_count)
        self.qubits_count.setValidator(validator)
        self.qubits_count.editingFinished.connect(self.on_qubits_count_changed)
        self.grid.addWidget(self.qubits_count, 0, 3, 1, 1)

        self.stopped()

    def on_run_release(self):
        self.runSimulation.emit(0)

    def on_manual_release(self):
        self.runSimulation.emit(int(self.start_step.text()))

    def on_next_release(self):
        self.nextStep.emit()

    def on_stop_release(self):
        self.stopSimulation.emit()

    def on_simulation_start(self):
        self.running()

    def on_simulation_update(self, status, step, total):
        self.set_simulation_status(status)
        self.current_step = step
        self.total_steps = total
        self.update_labels()

    def on_simulation_end(self):
        self.simulation_status = "-"
        self.current_step = "-"
        self.total_steps = "-"
        self.stopped()
        self.update_labels()

    def on_step_changed(self):
        result = self.start_step.validator().validate(self.start_step.text(), 0)
        if result[0] != QIntValidator.Acceptable:
            self.start_step.setText(str(config.INITIAL_LAYERS_COUNT))

    def on_resize_release(self):
        self.qubitCountChange.emit(int(self.qubits_count.text()))

    def on_qubits_count_changed(self):
        result = self.start_step.validator().validate(self.start_step.text(), 0)
        if result[0] != QIntValidator.Acceptable:
            self.start_step.setText(str(config.INITIAL_QUBITS))

    def running(self):
        self.run.setDisabled(True)
        self.manual.setDisabled(True)
        self.resize.setDisabled(True)
        self.next.setDisabled(False)
        self.stop.setDisabled(False)

    def stopped(self):
        self.run.setDisabled(False)
        self.manual.setDisabled(False)
        self.resize.setDisabled(False)
        self.next.setDisabled(True)
        self.stop.setDisabled(True)

    def set_simulation_status(self, status):
        if status:
            self.simulation_status = "Running..."
        else:
            self.simulation_status = "-"

    def update_labels(self):
        self.status.setText("Status: " + self.simulation_status)
        self.step.setText("Step: " + str(self.current_step))
        self.total.setText("Total: " + str(self.total_steps))


        
