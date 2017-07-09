from Scheduler.Controllers.MainController import MainWindow

from PyQt5 import QtWidgets
import sys

import logging

#
formatter = logging.Formatter(fmt='%(levelname)s:%(module)s:%(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

app = QtWidgets.QApplication(sys.argv)
ex = MainWindow()
sys.exit(app.exec_())
