from CircuitElement import CircuitElement
from PyQt5.QtCore import pyqtSignal

class RegisterButton(CircuitElement):
    """description of class"""

    stateChanged = pyqtSignal()

    def __init__(self, index, **kwargs):
        super().__init__(**kwargs)
        self.value = 0
        self.index = index

    def mouseReleaseEvent(self, QMouseEvent):
        self.value = 1 - self.value
        self.set_state(str(self.value))
        self.stateChanged.emit()
        


