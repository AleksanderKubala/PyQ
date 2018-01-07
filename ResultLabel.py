from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt

from config import label_height, label_width, label_line_width

class ResultLabel(QLabel):
    """description of class"""

    def __init__(self, text, width = label_width, height = label_height, shape = None, shadow = None, **kwargs):
        super().__init__(**kwargs)
        self.setText(text)
        self.setFixedSize(width, height)
        self.setLineWidth(label_line_width)
        self.setAlignment(Qt.AlignCenter)
        if shape is not None: self.setFrameShape(shape)
        if shadow is not None: self.setFrameShadow(shadow)



