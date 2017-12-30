from PyQt5.QtWidgets import QFrame, QGridLayout, QScrollArea
from PyQt5.QtCore import Qt
from ResultLabel import ResultLabel
from GridFrame import GridFrame

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
        amplitude = ResultLabel(str(result.amplitude))
        bits = ResultLabel(str(result.bits))
        probability = ResultLabel(str(result.probability))
        return [amplitude, bits, probability]


