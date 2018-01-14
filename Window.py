from PyQt5.QtWidgets import QGridLayout, QFrame, QWidget
from GateFrame import GateFrame
from GateButton import GateButton
from CircuitFrame import CircuitFrame
from RegisterFrame import RegisterFrame
from ActionFrame import ActionFrame
from ResultsFrame import ResultsFrame
import config


class Window(QWidget):
    
    height = config.win_height
    width = config.win_width

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.initUI()

    def initUI(self):
        self.basegate = GateFrame(cols = 6, spacing = 0, margins = (0, 0, 0, 0))
        self.basegate.setFrameShape(QFrame.Panel)
        self.basegate.setFrameShadow(QFrame.Sunken)
        self.results = ResultsFrame()
        self.results.setFrameShape(QFrame.Panel)
        self.results.setFrameShadow(QFrame.Sunken)
        self.register = RegisterFrame(config.INITIAL_QUBITS, 1, 0, (0, 0, 0, 0))
        self.circuit = CircuitFrame(config.INITIAL_QUBITS, config.INITIAL_LAYERS_COUNT, 0, (0, 0, 0, 0))
        self.actions = ActionFrame(rows = 6, cols = 7)
        self.actions.setFrameShape(QFrame.Panel)
        self.actions.setFrameShadow(QFrame.Sunken)

        circuitframe = QFrame()
        circuitframe.setFrameShape(QFrame.Panel)
        circuitframe.setFrameShadow(QFrame.Sunken)
        circuit_grid = QGridLayout()
        circuit_grid.setSpacing(0)
        circuit_grid.setContentsMargins(0, 0, 0, 0)
        circuitframe.setLayout(circuit_grid)
        circuit_grid.addWidget(self.register, 0, 1, 3, 1)
        circuit_grid.addWidget(self.circuit, 0, 2, 3, 8)

        names = [config.X, config.Y, config.Z, config.HADAMARD,config.S, config.S + config.HERM, config.T, config.T + config.HERM, config.SWAP, config.CONTROL]
        buttons = []
        for name in names:
            button = GateButton(name)
            buttons.append(button)
        self.basegate.add_widgets(buttons)

        grid = QGridLayout()
        spacing = QGridLayout.spacing(grid)
        grid.setContentsMargins(2, spacing, 2, spacing)
        grid.setHorizontalSpacing(1)
        self.setLayout(grid)

        grid.addWidget(self.basegate, 0, 0, 1, 3)
        grid.addWidget(self.results, 1, 0, 7, 3)
        grid.addWidget(circuitframe, 0, 3, 6, 9)
        grid.addWidget(self.actions, 6, 3, 2, 9)

        self.setGeometry(300, 300, 1024, 768)
