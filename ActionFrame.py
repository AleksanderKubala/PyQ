from GridFrame import GridFrame
from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel, QCheckBox
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtCore import pyqtSignal, Qt, QLocale
import config

class ActionFrame(GridFrame):
    """description of class"""

    allowDisturbances = pyqtSignal(object, float)
    disturbanceProbability = pyqtSignal(float)
    qubitDistProbability = pyqtSignal(float)
    rotationProbability = pyqtSignal(float)
    runSimulation = pyqtSignal(int)
    nextStep = pyqtSignal()
    stopSimulation = pyqtSignal()
    qubitCountChange = pyqtSignal(int)

    def __init__(self, rows = 0, cols = 0, spacing = None, margins = None, **kwargs):
        super().__init__(rows, cols, spacing, margins, **kwargs)
        self.simulation_status = '-'
        self.current_step = '-'
        self.total_steps = '-'

        self.grid.setColumnStretch(0, 1)
        self.grid.setColumnStretch(1, 1)
        self.grid.setColumnStretch(2, 1)
        self.grid.setColumnStretch(3, 1)
        self.grid.setColumnStretch(4, 1)

        self.locale = QLocale(QLocale.English, QLocale.UnitedStates)
        self.prob_validator = QDoubleValidator(0.0, 1.0, 5)
        self.prob_validator.setLocale(self.locale)
        self.size_validator = QIntValidator(1, config.SIZE_RESTRICTION)
        self.size_validator.setRange(1, config.SIZE_RESTRICTION)
        self.step_validator = QIntValidator(1, config.INITIAL_LAYERS_COUNT)
        self.step_validator.setRange(1, config.INITIAL_LAYERS_COUNT)

        self.run = QPushButton("Run Simulation")
        self.run.released.connect(self.on_run_release)
        self.grid.addWidget(self.run, 0, 0, 1, 1)

        self.manual = QPushButton("Run Manually From")
        self.manual.released.connect(self.on_manual_release)
        self.grid.addWidget(self.manual, 1, 0, 1, 1)

        self.start_step = QLineEdit(str(config.INITIAL_LAYERS_COUNT))
        self.start_step.editingFinished.connect(self.on_step_change)
        self.grid.addWidget(self.start_step, 1, 1, 1, 1)

        self.next = QPushButton("Next")
        self.next.released.connect(self.on_next_release)
        self.grid.addWidget(self.next, 2, 0, 1, 1)

        self.stop = QPushButton("Stop")
        self.stop.released.connect(self.on_stop_release)
        self.grid.addWidget(self.stop, 2, 1, 1, 1)

        self.status = QLabel("Status: " + self.simulation_status)
        self.grid.addWidget(self.status, 3, 0, 1, 1)

        self.step = QLabel("Step: " + self.current_step)
        self.grid.addWidget(self.step, 4, 0, 1, 1)

        self.total = QLabel("Total: " + self.total_steps)
        self.grid.addWidget(self.total, 4, 1, 1, 1)

        self.resize = QPushButton("Resize Register")
        self.resize.released.connect(self.on_resize_release)
        self.grid.addWidget(self.resize, 0, 3, 1, 1)

        self.qubits_count = QLineEdit(str(config.INITIAL_QUBITS))
        self.qubits_count.editingFinished.connect(self.on_qubits_count_change)
        self.grid.addWidget(self.qubits_count, 0, 4, 1, 1)

        self.ideal = QCheckBox("Ideal Circuit")
        self.ideal.setCheckable(True)
        self.ideal.setChecked(True)
        self.ideal.stateChanged.connect(self.on_allow_disturbances)
        self.grid.addWidget(self.ideal, 1, 3, 1, 1)

        self.disturbance_prob_label = QLabel("Disturbance prob.:")
        self.grid.addWidget(self.disturbance_prob_label, 2, 3, 1, 1)

        self.disturbance_prob = QLineEdit(str(config.DISTURBANCE_PROBABILITY))
        self.disturbance_prob.editingFinished.connect(self.on_disturbance_prob_change)
        self.disturbance_prob.setDisabled(True)
        self.grid.addWidget(self.disturbance_prob, 2, 4, 1, 1)

        self.qubit_disturbance_label = QLabel("Qubit dist. prob.:")
        self.grid.addWidget(self.qubit_disturbance_label, 3, 3, 1, 1)

        self.qubit_disturbance = QLineEdit(str(config.QUBIT_DISTURBANCE_PROBABILITY))
        self.qubit_disturbance.editingFinished.connect(self.on_qubit_disturbance_change)
        self.qubit_disturbance.setDisabled(True)
        self.grid.addWidget(self.qubit_disturbance, 3, 4, 1, 1)

        self.rotation_prob_label = QLabel("Rotation prob.:")
        self.grid.addWidget(self.rotation_prob_label, 4, 3, 1, 1)

        self.rotation_prob = QLineEdit(str(config.ROTATION_PROBABILITY))
        self.rotation_prob.editingFinished.connect(self.on_rotation_prob_change)
        self.rotation_prob.setDisabled(True)
        self.grid.addWidget(self.rotation_prob, 4, 4, 1, 1)

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

    def on_step_change(self):
        result = self.step_validator.validate(self.start_step.text(), 0)
        if result[0] != QIntValidator.Acceptable:
            self.start_step.setText(str(config.INITIAL_LAYERS_COUNT))

    def on_resize_release(self):
        self.qubitCountChange.emit(int(self.qubits_count.text()))

    def on_qubits_count_change(self):
        result = self.size_validator.validate(self.qubits_count.text(), 0)
        if result[0] != QIntValidator.Acceptable:
            self.qubits_count.setText(str(config.INITIAL_QUBITS))

    def on_allow_disturbances(self, state):
        if state == Qt.Unchecked:
            self.disturbance_prob.setDisabled(False)
            self.qubit_disturbance.setDisabled(False)
            self.rotation_prob.setDisabled(False)
            self.allowDisturbances.emit(False, float(self.disturbance_prob.text()))
        if state == Qt.Checked:
            self.disturbance_prob.setDisabled(True)
            self.qubit_disturbance.setDisabled(True)
            self.rotation_prob.setDisabled(True)
            self.allowDisturbances.emit(True, float(self.disturbance_prob.text()))

    def on_disturbance_prob_change(self):
        result = self.prob_validator.validate(self.disturbance_prob.text(), 0)
        if result[0] != QDoubleValidator.Acceptable:
            self.disturbance_prob.setText(str(config.DISTURBANCE_PROBABILITY))
        self.disturbanceProbability.emit(float(self.disturbance_prob.text()))

    def on_qubit_disturbance_change(self):
        result = self.prob_validator.validate(self.qubit_disturbance.text(), 0)
        if result[0] != QDoubleValidator.Acceptable:
            self.qubit_disturbance.setText(str(config.QUBIT_DISTURBANCE_PROBABILITY))
        self.qubitDistProbability.emit(float(self.qubit_disturbance.text()))

    def on_rotation_prob_change(self):
        result = self.prob_validator.validate(self.rotation_prob.text(), 0)
        if result[0] != QDoubleValidator.Acceptable:
            self.rotation_prob.setText(str(config.ROTATION_PROBABILITY))
        self.rotationProbability.emit(float(self.rotation_prob.text()))

    def running(self):
        self.run.setDisabled(True)
        self.manual.setDisabled(True)
        self.resize.setDisabled(True)
        self.next.setDisabled(False)
        self.stop.setDisabled(False)
        dist_allowed = self.ideal.checkState()
        if dist_allowed == Qt.Unchecked:
            self.disturbance_prob.setDisabled(True)
            self.qubit_disturbance.setDisabled(True)
            self.rotation_prob.setDisabled(True)
        self.ideal.setDisabled(True)

    def stopped(self):
        self.run.setDisabled(False)
        self.manual.setDisabled(False)
        self.resize.setDisabled(False)
        self.next.setDisabled(True)
        self.stop.setDisabled(True)
        self.ideal.setDisabled(False)
        dist_allowed = self.ideal.checkState()
        if dist_allowed == Qt.Unchecked:
            self.disturbance_prob.setDisabled(False)
            self.qubit_disturbance.setDisabled(False)
            self.rotation_prob.setDisabled(False)

    def set_simulation_status(self, status):
        if status:
            self.simulation_status = "Running..."
        else:
            self.simulation_status = "-"

    def update_labels(self):
        self.status.setText("Status: " + self.simulation_status)
        self.step.setText("Step: " + str(self.current_step))
        self.total.setText("Total: " + str(self.total_steps))


        
