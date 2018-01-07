from GridFrame import GridFrame
from GateSlot import GateSlot
from PyQt5.QtCore import pyqtSignal, Qt
from Addition import Addition

import config

class CircuitFrame(GridFrame):
    """description of class"""

    removalRequested = pyqtSignal(int, int)
    additionRequested = pyqtSignal(object)

    def __init__(self, rows = 0, cols = 0, spacing = None, margins = None, **kwargs):
        super().__init__(rows, cols, spacing, margins, **kwargs)
        self.grid.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.add_rows(self.size[0])
        self.multi_begin = None
        self.current_gate = None
        self.setStyleSheet("background-color: rgb(255, 255, 255)")

    def add_rows(self, count):
        elements = []
        for i in range(self.slot[0], self.slot[0] + count):
            for j in range(self.size[1]):
                gateslot = GateSlot(i, j)
                gateslot.set_state(config.EMPTY)
                elements.append(gateslot)
            self.add_widgets(elements)
            elements = []

    def add_widgets(self, widgets, by_cols = True):
        widgets = super().add_widgets(widgets, by_cols)
        for i in range(len(widgets)):
            widgets[i].setGate.connect(self.on_setGate)
            widgets[i].destroyGate.connect(self.on_destroyGate)

    def on_setGate(self, arg):
        sender = self.sender()
        if self.current_gate is not None:
            if self.current_gate != config.CONTROL and self.current_gate != config.SWAP:
                request = Addition(self.current_gate, sender.row, sender.col)
                self.additionRequested.emit(request)
            else:
                self.set_multi_qubit_gate(sender)

    def on_destroyGate(self):
        if self.multi_begin is None:
            sender = self.sender()
            self.removalRequested.emit(sender.row, sender.col)
        else:
            self.deactivate_slot(self.multi_begin)
            self.multi_begin = None

    def on_circuit_change(self, changes):
        for removal in changes.removed:
            for index in removal[1]:
                slot = self.grid.itemAt(index*self.size[1] + removal[0]).widget()
                slot.links.clear()
                slot.set_state(config.EMPTY)
        for addition in changes.added:
            for i in range(addition[1].first, addition[1].last + 1):
                if addition[1].first != addition[1].last:
                    if i == addition[1].first: modifier = config.DOWN
                    elif i < addition[1].last: modifier = config.MID
                    else: modifier = config.UP
                else: modifier = ""
                slot = self.grid.itemAt(i*self.size[1] + addition[1].layer).widget()
                self.deactivate_slot(slot)
                if slot.row in addition[1].controls: slot.set_state(config.CONTROL, modifier)
                elif slot.row in addition[1].qubits: slot.set_state(addition[1].basegate, modifier)
                else: slot.set_state(config.EMPTY, modifier)

    def deactivate_slot(self, slot):
        slot.frozen = False
        slot.active = False
        slot.update()

    def on_gateChanged(self, signature):
        self.current_gate = signature
        if self.multi_begin is not None:
            self.deactivate_slot(self.multi_begin)
            self.multi_begin = None

    def on_circuitResized(self, new_size):
        count = new_size - self.size[0]
        if count > 0:
            self.add_rows(count)
            self.size[0] = self.size[0] + count
        elif count < 0:
            self.remove_grid_line(new_size)
        

    def set_multi_qubit_gate(self, source):
        if self.multi_begin is None:
            if source.state != config.EMPTY or self.current_gate == config.SWAP:
                    self.multi_begin = self.get_base(source)
                    source.frozen = True
        else:
            if source.col == self.multi_begin.col:
                if source.row != self.multi_begin.row:
                    self.link_slots(source)
                    qubits, controls = self.get_controls_and_qubits(source)
                    if self.current_gate != config.SWAP:
                        request = Addition(self.multi_begin.state, qubits, self.multi_begin.col, controls)
                    else:
                        request = Addition(self.current_gate, qubits, self.multi_begin.col, controls)
                    self.multi_begin.frozen = False
                    self.multi_begin = None
                    self.additionRequested.emit(request)

    def link_slots(self, end):
        end.links.add(self.multi_begin)
        for link in self.multi_begin.links:
            end.links.add(link)
            link.links.add(end)
        self.multi_begin.links.add(end)

    def get_controls_and_qubits(self, end):
        qubits, controls = [], []
        for link in self.multi_begin.links:
            if link.state == self.multi_begin.state:
                if link.state == config.SWAP:
                    qubits.append(link.row)
            if link.state == config.CONTROL:
                controls.append(link.row)
        if self.current_gate == config.CONTROL:
            controls.append(end.row)
        if self.current_gate == config.SWAP:
            qubits.append(end.row)
        qubits.append(self.multi_begin.row)
        return qubits, controls

    def get_base(self, source):
        base = None
        for link in source.links:
            if link.state != config.CONTROL:
                base = link
        if base is None:
            base = source
        return base

        





    


