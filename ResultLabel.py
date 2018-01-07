from PyQt5.QtWidgets import QLabel, QFrame
from PyQt5.QtCore import Qt

from config import label_height, label_width, label_line_width

class ResultLabel(QLabel):
    """description of class"""

    def __init__(self, text, width = label_width, height = label_height, **kwargs):
        super().__init__(**kwargs)
        self.setText(text)
        self.setFixedSize(width, height)
        self.setLineWidth(label_line_width)
        self.setAlignment(Qt.AlignCenter)


