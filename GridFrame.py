from PyQt5.QtWidgets import QGridLayout,  QFrame
from PyQt5.QtCore import Qt
from GateButton import GateButton

class GridFrame(QFrame):
    """description of class"""

    def __init__(self, rows = 0, cols = 0, spacing = None, margins = None, **kwargs):
        super().__init__(**kwargs)
        self.grid = QGridLayout()
        if margins is not None: self.grid.setContentsMargins(margins[0], margins[1], margins[2], margins[3])
        if spacing is not None: self.grid.setSpacing(spacing)
        self.setLayout(self.grid)
        #self.constant_size = [False if rows == 0 else True, False if cols == 0 else True]
        self.size = [rows, cols]
        self.slot = [0, 0]

    def remove_grid_line(self, new_size, by_cols = True):
        idx_check = self._get_slot_index_check(by_cols)
        self.slot[1 - idx_check] = self.size[1 - idx_check] - 1
        self.slot[idx_check] = self.size[idx_check] - 1
        for i in range(self.slot[1 - idx_check], new_size - 1, -1):
            for j in range(self.slot[idx_check], -1, -1):
                item = self.grid.itemAt(self.size[idx_check]*i + j)
                widget = item.widget()
                self.grid.removeWidget(widget)
                widget.setParent(None)
            self.slot[1 - idx_check] = self.slot[1 - idx_check] - 1
            self.slot[idx_check] = self.size[idx_check] - 1
        self.slot[1 - idx_check] = new_size
        self.slot[idx_check] = 0
        self.size[1 - idx_check] = new_size
        self.update()


    def add_widgets(self, widgets, by_cols = True):
        widgets = widgets if type(widgets) is list or type(widgets) is tuple else [widgets]
        idx_check = self._get_slot_index_check(by_cols)
        limits = self._grid_limits(widgets)
        for i in range(len(widgets)):
            self.grid.addWidget(widgets[i], self.slot[0], self.slot[1])
            self._calculate_new_slot(limits, idx_check)
        return widgets

    #do poprawki
    def _grid_limits(self, widgets):
        row_limit = 0
        col_limit = 0
        if self.size[0] > 0: row_limit = self.size[0]
        else: row_limit = self.slot[0] + len(widgets)
        if self.size[1] > 0: col_limit = self.size[1]
        else: col_limit = self.slot[1] + len(widgets)
        return (row_limit, col_limit)

    def _calculate_new_slot(self, limits, idx_check):
        self.slot[idx_check] = self.slot[idx_check] + 1
        if self.slot[idx_check] >= limits[idx_check]:
            self.slot[idx_check] = 0
            self.slot[1 - idx_check] = self.slot[1 - idx_check] + 1

    def _get_slot_index_check(self, by_cols):
        if by_cols: return 1
        else: return 0





