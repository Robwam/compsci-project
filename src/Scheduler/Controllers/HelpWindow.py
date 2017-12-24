from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui

'''
Help window controller
'''
class HelpWindow(QMainWindow):
    def __init__(self, parent=None):
        super(HelpWindow, self).__init__(parent)
        self.setup_ui()

    '''
    Creates UI structure
    '''
    def setup_ui(self):
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(QLabel("Help Page"))

        self.setLayout(self.hbox)
