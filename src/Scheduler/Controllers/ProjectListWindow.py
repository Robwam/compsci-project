import Scheduler.Configuration.database as database
import pony.orm

from functools import partial

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui

from Scheduler.Controllers.ProjectWindow import ProjectWindow
from Scheduler.Models.Project import Project


class ProjectListWindow(QWidget):
    def __init__(self, parent=None):
        super(ProjectListWindow, self).__init__(parent)

        database.setup()

        # Add new button
        self.open_project_button = QPushButton("New project")
        self.open_project_button.clicked.connect(self.open_project)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(['Name', 'Date', 'Open'])
        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_widget.setSelectionMode(QTableWidget.NoSelection)
        self.table_widget.setShowGrid(False)

        # Fix headers
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(0, header.Stretch)
        header.setSectionResizeMode(1, header.ResizeToContents)
        header.setSectionResizeMode(2, header.ResizeToContents)

        # Add projects to table
        self.populate_projects()

        # Add new button
        self.open_project_button = QPushButton("New project")
        self.open_project_button.clicked.connect(self.open_new_project)

        # Main hbox
        vbox = QVBoxLayout()
        vbox.addWidget(QLabel("Projects"))
        vbox.addWidget(self.table_widget)
        vbox.addWidget(self.open_project_button)

        self.setLayout(vbox)

        self.show()

    @pony.orm.db_session
    def populate_projects(self):
        projects = Project.select()

        self.table_widget.setRowCount(len(projects))

        for i, project in enumerate(projects):
            open_button = QPushButton("Open", self.table_widget)
            open_button.clicked.connect(partial(self.open_project, project.get_pk()))
            self.table_widget.setCellWidget(i, 0, QLabel(project.name))
            self.table_widget.setCellWidget(i, 1, QLabel('12/03/17'))
            self.table_widget.setCellWidget(i, 2, open_button)

    def open_project(self, project_id):
        print(project_id)
        project_window = ProjectWindow(self, project_id=project_id)
        project_window.show()

    @pony.orm.db_session
    def open_new_project(self):
        project = Project(name="New Project")

        # NOTE we commit so that we have a primary key
        pony.orm.commit()

        self.open_project(project.get_pk())
