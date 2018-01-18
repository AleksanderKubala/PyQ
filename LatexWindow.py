from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QMainWindow
from qtpy import QtGui

import config


class LatexWindow(QMainWindow):

    def __init__(self, parent):
        super().__init__(parent)
        self.setGeometry(300, 300, config.latex_win_width, config.latex_win_height)
        self.layout().setAlignment(Qt.AlignLeft)

    def resizeEvent(self, a0: QtGui.QResizeEvent):
        count = self.layout().count()
        for i in range(count):
            widget = self.layout().itemAt(i).widget()
            widget.resize(self.width(), self.height())
            widget.repaint()
