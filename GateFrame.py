from GridFrame import GridFrame 
from PyQt5.QtCore import pyqtSignal, Qt

class GateFrame(GridFrame):
    """description of class"""

    gateChanged = pyqtSignal(object)

    def __init__(self, rows = 0, cols = 0, spacing = None, margins = None, **kwargs):
        super().__init__(rows, cols, spacing, margins, **kwargs)
        self.grid.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.active_gate = None

    def add_widgets(self, widgets, by_cols = True):
        widgets = super().add_widgets(widgets, by_cols)
        for i in range(len(widgets)):
            widgets[i].toggled.connect(self.on_toggle)

    def on_toggle(self, bool = 0):
        sender = self.sender()
        if self.active_gate is not None:
            self.active_gate.uncheck()
        self.active_gate = None
        signature = None
        if sender.isChecked():
            self.active_gate = sender
            signature = self.active_gate.signature
        self.gateChanged.emit(signature)
        return True

    def get_active_gate(self):
        return self.active_gate.signature

    def on_simulation_start(self):
        count = self.grid.count()
        for i in range(count):
            self.grid.itemAt(i).widget().setDisabled(True)

    def on_simulation_stop(self):
        count = self.grid.count()
        for i in range(count):
            self.grid.itemAt(i).widget().setDisabled(False)


    


