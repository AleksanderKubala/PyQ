from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QColor, QIcon, QPainter
from PyQt5.QtCore import QSize, Qt
from Icons import Icons

class CircuitElement(QPushButton):
    """description of class"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setFixedSize(48, 48)
        self.setIconSize(QSize(48, 48))
        self._state = None
        self._modifier = ""
        self.type = ""
        self.active = False
        self.frozen = False

    @property
    def state(self):
        return self._state

    @property
    def mod_state(self):
        return self._state + self.type + self._modifier

    def set_state(self, state, modifier = ""):
        self._state = state
        self._modifier = modifier
        self.setIcon(Icons.get_icon(self.mod_state))

    def set_type(self, type):
        self.type = type
        self.setIcon(Icons.get_icon(self.mod_state))

    def enterEvent(self, QEvent):
        if self.frozen == False:
            self.active = True
            self.update()

    def leaveEvent(self, QEvent):
        if self.frozen == False:
            self.active = False
            self.update()

    def paintEvent(self, QPaintEvent):
        painter = QPainter()
        icon = self.icon()
        painter.begin(self)
        if self.active == True:
            icon.paint(painter, QPaintEvent.rect(), mode = QIcon.Active)
        else:
            icon.paint(painter, QPaintEvent.rect(), mode = QIcon.Normal)
        painter.end()

