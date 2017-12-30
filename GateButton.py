from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QPalette, QColor


class GateButton(QPushButton):
    """description of class"""

    def __init__(self, signature, **kwargs):
        super().__init__(**kwargs)
        self.signature = signature
        self.setText(signature.upper())
        self.setFixedSize(48, 48)
        self.setCheckable(True)
    
    def mousePressEvent(self, QMouseEvent):
        if self.isChecked():
            self.setChecked(False)
        else:
            self.setChecked(True)
        self.update()

    def uncheck(self):
        self.setChecked(False)

    def check(self):
        self.setChecked(True)





