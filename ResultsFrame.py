from PyQt5.QtWidgets import QFrame, QGridLayout, QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QResizeEvent, QPalette
from ResultLabel import ResultLabel
from GridFrame import GridFrame
from ResultLatexLabel import ResultLatexLabel
from sympy import *


class ResultsFrame(QFrame):
    """description of class"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = QGridLayout()
        self.layout.setGeometry(self.rect())
        self.layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.layout.addWidget(ResultLabel("Amplitudes", shadow = QFrame.Raised), 0, 0)
        self.layout.addWidget(ResultLabel("Bits", shadow = QFrame.Raised), 0, 1)
        self.layout.addWidget(ResultLabel("Probability(%)", shadow = QFrame.Raised), 0, 2)
        self.resultsgrid = GridFrame(cols = 3, spacing = 0, margins = (0, 0, 0, 0))
        self.resultsgrid.grid.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setGeometry(self.x(), self.y() + 24, self.width(), self.height() - 24)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.resultsgrid)
        self.layout.addWidget(self.scrollArea, 1, 0, 1, 3)

    def prepare_results(self, results):
        prepared = []
        for result in results:
            prepared = prepared + self._create_result_row(result)
        return prepared
        

    def on_resultsRetrieved(self, results):
        self.resultsgrid.remove_grid_line(0)
        self.resultsgrid.update()
        self.resultsgrid.size[0] = len(results)
        prepared = self.prepare_results(results)
        self.resultsgrid.add_widgets(prepared)

    def _create_result_row(self, result):
        color = self.palette().color(QPalette.Background)
        amplitude = ResultLatexLabel(result.amplitude, color)
        #amplitude = ResultLabel(latex(sympify(result.amplitude)))
        bits = ResultLabel(str(result.bits), self.width()/self.layout.columnCount())
        probability = ResultLabel(str(result.probability), self.width()/self.layout.columnCount())
        return [amplitude, bits, probability]

    def resizeEvent(self, a0: QResizeEvent):

        self.scrollArea.resize(self.width(), self.height())
        self.resultsgrid.resize(self.width(), self.height())
        #column_count = self.layout.columnCount()
        #for i in range(3, self.resultsgrid.layout().count()):
        #    item = self.resultgrid.layout().itemAt(i)
        #    rect = item.geometry()
        #    rect.setWidth(self.width()//column_count)
        #    item.setGeometry(rect)











