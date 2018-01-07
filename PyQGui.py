from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication
from App import App
import sys

app = QApplication(sys.argv)
ex = App()
QCoreApplication.exit(app.exec_())