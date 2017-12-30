from CircuitElement import CircuitElement
from PyQt5.QtCore import pyqtSignal, Qt

class GateSlot(CircuitElement):
    """description of class"""

    setGate = pyqtSignal(object)
    destroyGate = pyqtSignal()

    def __init__(self, row, col, **kwargs):
        super().__init__(**kwargs)
        self.row = row
        self.col = col
        self.links = set()
    
    def mouseReleaseEvent(self, QMouseEvent):
        button = QMouseEvent.button()
        if button == Qt.RightButton:
            self.destroyGate.emit()
        elif button == Qt.LeftButton:
            self.setGate.emit(None)



        

    




