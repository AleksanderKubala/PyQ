from GridFrame import GridFrame
from RegisterButton import RegisterButton
from PyQt5.QtCore import pyqtSignal, Qt
import config

class RegisterFrame(GridFrame):
    """description of class"""

    registerChanged = pyqtSignal(int)
    registerResized = pyqtSignal(int)

    def __init__(self, rows = 0, cols = 0, spacing = None, margins = None, **kwargs):
        super().__init__(rows, cols, spacing, margins, **kwargs)
        self.grid.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.add_rows(self.size[0])
        self.register = [0]*rows
        self.setStyleSheet("background-color: rgb(255, 255, 255)")

    def add_rows(self, count):
        qubits = []
        for i in range(self.grid.count(), self.grid.count() + count):
            qubit = RegisterButton(i)
            qubit.set_state(config.ZERO)
            qubits.append(qubit)
        self.add_widgets(qubits)

    def add_widgets(self, widgets, by_cols = True):
        widgets = super().add_widgets(widgets, by_cols)
        for i in range(len(widgets)):
            widgets[i].stateChanged.connect(self.on_state_change, Qt.UniqueConnection)

    def register_to_int(self):
        value = int(''.join(map(str, self.register)), 2)
        return value   

    def on_state_change(self):
        sender = self.sender()
        self.register[sender.index] = sender.value
        self.registerChanged.emit(self.register_to_int())

    def on_qubitCountChange(self, new_size):
        count = new_size - self.size[0]
        if count > 0:
            self.add_rows(count)
            self.register = self.register + [0]*count
            self.size[0] = self.size[0] + count
        elif count < 0:
            self.remove_grid_line(new_size)
            self.register = self.register[:new_size]
        self.registerResized.emit(new_size)
        
        






