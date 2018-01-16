from PyQt5.QtWidgets import QFrame, QGridLayout, QScrollArea, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette
from ResultLabel import ResultLabel
from GridFrame import GridFrame
from ResultLatexLabel import ResultLatexLabel
import config
from sympy import *


class ResultsFrame(QFrame):
    """description of class"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.measurements = "-"
        self.layout = QGridLayout()
        self.layout.setGeometry(self.rect())
        self.layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        measurement_label = QLabel("Measurement")
        measurement_label.setFixedHeight(config.label_height)
        measurement_label.setFrameShadow(QFrame.Raised)
        measurement_label.setFrameShape(QFrame.Panel)
        measurement_label.setAlignment(Qt.AlignCenter)
        self.measurement_values = QLabel(self.measurements)
        self.measurement_values.setFixedHeight(config.label_height)
        self.measurement_values.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(measurement_label, 0, 0, 1, 3)
        self.layout.addWidget(self.measurement_values, 1, 0, 1, 3)
        self.layout.addWidget(ResultLabel("Amplitudes", shape = QFrame.Panel, shadow = QFrame.Raised), 2, 0)
        self.layout.addWidget(ResultLabel("Bits", shape = QFrame.Panel, shadow = QFrame.Raised), 2, 1)
        self.layout.addWidget(ResultLabel("Probability(%)", shape = QFrame.Panel, shadow = QFrame.Raised), 2, 2)
        self.resultsgrid = GridFrame(cols = 3, spacing = 0, margins = (0, 0, 0, 0))
        self.resultsgrid.grid.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setGeometry(self.x(), self.y() + 72, self.width(), self.height() - 72)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.resultsgrid)
        self.layout.addWidget(self.scrollArea, 3, 0, 1, 3)

    def prepare_results(self, results):
        prepared = []
        for result in results:
            prepared = prepared + self._create_result_row(result)
        return prepared


    def on_resultsRetrieved(self, results, measurements):
        self.resultsgrid.remove_grid_line(0)
        self.resultsgrid.update()
        self.resultsgrid.size[0] = len(results)
        prepared = self.prepare_results(results)
        self.resultsgrid.add_widgets(prepared)
        self.measurements = measurements
        self.measurement_values.setText(self.measurements)


    def _create_result_row(self, result):
        color = self.palette().color(QPalette.Background)
        amplitude = ResultLatexLabel(result.amplitude, color)
        bits = ResultLabel(str(result.bits), self.width()/self.layout.columnCount())
        probability = ResultLabel(str(result.probability), self.width()/self.layout.columnCount())
        return [amplitude, bits, probability]












