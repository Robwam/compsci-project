from Scheduler.Controllers.MainController import MainController

from PyQt5 import QtWidgets
import sys


app = QtWidgets.QApplication(sys.argv)
ex = MainController()
sys.exit(app.exec_())
