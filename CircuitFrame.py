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
        self.mutable = True

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
        if self.mutable:
            sender = self.sender()
            if self.current_gate is not None:
                if self.current_gate != config.CONTROL and self.current_gate != config.SWAP:
                    if sender.type != config.CLASSICAL:
                        request = Addition(self.current_gate, sender.row, sender.col)
                        self.additionRequested.emit(request)
                else:
                    self.set_multi_qubit_gate(sender)

    def on_destroyGate(self):
        if self.mutable:
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
                if slot.state == config.MEASUREMENT:
                    self.measurement_changes(self.get_all_in_row(slot.row, begin=slot.col+1))
                slot.set_state(config.EMPTY)
        for addition in changes.added:
            slots = []
            j = 0
            for i in range(addition[1].first, addition[1].last + 1):
                slots.append(self.grid.itemAt(i*self.size[1] + addition[1].layer).widget())
            self.link_slots(slots)
            for i in range(addition[1].first, addition[1].last + 1):
                if addition[1].first != addition[1].last:
                    if i == addition[1].first: modifier = config.DOWN
                    elif i < addition[1].last: modifier = config.MID
                    else: modifier = config.UP
                else: modifier = ""
                slot = slots[j]
                self.deactivate_slot(slot)
                if slot.row in addition[1].controls: slot.set_state(config.CONTROL, modifier)
                elif slot.row in addition[1].qubits:
                    slot.set_state(addition[1].basegate, modifier)
                    if slot.state == config.MEASUREMENT:
                        self.measurement_changes(self.get_all_in_row(slot.row, begin=slot.col + 1))
                else: slot.set_state(config.EMPTY, modifier)
                j += 1

    def measurement_changes(self, widgets):
        for widget in widgets:
            if widget.type == config.QUANTUM:
                widget.set_type(config.CLASSICAL)
            else:
                widget.set_type(config.QUANTUM)

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
            if (source.state != config.EMPTY or self.current_gate == config.SWAP) and source.state != config.MEASUREMENT:
                    self.multi_begin = self.get_base(source)
                    source.frozen = True
        else:
            if source.col == self.multi_begin.col:
                if source.row != self.multi_begin.row:
                    qubits, controls = self.get_controls_and_qubits(source)
                    if self.current_gate != config.SWAP:
                        request = Addition(self.multi_begin.state, qubits, self.multi_begin.col, controls)
                    else:
                        request = Addition(self.current_gate, qubits, self.multi_begin.col, controls)
                    self.multi_begin.frozen = False
                    self.multi_begin = None
                    self.additionRequested.emit(request)

    def link_slots(self, slots):
        for slot in slots:
            for slot_ in slots:
                slot.links.add(slot_)

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

    def on_simulation_start(self):
        self.mutable = False

    def on_simulation_stop(self):
        self.mutable = True

        





    


