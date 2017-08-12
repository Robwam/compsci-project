#!/usr/bin/env python3

from Scheduler.Controllers.ProjectListWindow import ProjectListWindow

from PyQt5 import QtWidgets
import sys

app = QtWidgets.QApplication(sys.argv)
ex = ProjectListWindow()
sys.exit(app.exec_())
