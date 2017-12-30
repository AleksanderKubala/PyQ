from PyQt5.QtWidgets import QLabel, QFrame
from PyQt5.QtCore import Qt

class ResultLabel(QLabel):
    """description of class"""

    def __init__(self, text, shape = QFrame.Panel, shadow = QFrame.Sunken, **kwargs):
        super().__init__(**kwargs)
        self.setText(text)
        self.setFixedSize(96, 24)
        self.setLineWidth(1)
        self.setAlignment(Qt.AlignCenter)
        self.setFrameShape(shape)
        self.setFrameShadow(shadow)

