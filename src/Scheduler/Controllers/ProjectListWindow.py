import Scheduler.Configuration.database as database
import pony.orm

from functools import partial

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui

from Scheduler.Controllers.ProjectWindow import ProjectWindow
from Scheduler.Models.Project import Project
import Scheduler.Configuration.config as config

import os

'''
Project list window controller

Allows user to view and load projects from database
'''
class ProjectListWindow(QWidget):
    def __init__(self, parent=None):
        super(ProjectListWindow, self).__init__(parent)

        self.setGeometry(450, 300, 500, 400)
        self.setWindowTitle('Scheduler')

        database.setup()

        # Add new button
        self.open_project_button = QPushButton("New project")
        self.open_project_button.clicked.connect(self.open_project)

        # Add table
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(['Name', 'Date', 'Open', 'Delete'])
        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_widget.setSelectionMode(QTableWidget.NoSelection)
        self.table_widget.setShowGrid(False)

        # Fix headers
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(0, header.Stretch)
        header.setSectionResizeMode(1, header.ResizeToContents)
        header.setSectionResizeMode(2, header.ResizeToContents)
        header.setSectionResizeMode(3, header.ResizeToContents)

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

    '''
    Populate table with projects

    For each row add name, created time, open and delete button.
    '''
    @pony.orm.db_session
    def populate_projects(self):
        projects = Project.select()

        self.table_widget.setRowCount(len(projects))

        for i, project in enumerate(projects):

            open_button = QPushButton("Open", self.table_widget)
            open_button.clicked.connect(partial(self.open_project, project.get_pk()))

            delete_button = QPushButton("Delete", self.table_widget)
            delete_button.clicked.connect(partial(self.delete_project, project.get_pk()))

            self.table_widget.setCellWidget(i, 0, QLabel(project.name))
            self.table_widget.setCellWidget(i, 1, QLabel(project.created.strftime("%x")))
            self.table_widget.setCellWidget(i, 2, open_button)
            self.table_widget.setCellWidget(i, 3, delete_button)

    '''
    Handle open project events

    Args:
        Int project_id: The project ID of the project to load
    '''
    def open_project(self, project_id):
        project_window = ProjectWindow(self, project_id=project_id)
        project_window.show()

    '''
    Handle delete project events

    Args:
        Int project_id: The project ID of the project to load
    '''
    @pony.orm.db_session
    def delete_project(self, project_id):
        Project.get(id=project_id).delete()
        self.populate_projects() # Refresh list

    '''
    Handle new project events
    '''
    @pony.orm.db_session
    def open_new_project(self):
        project = Project(name="New Project")

        # NOTE we commit so that we have a primary key
        pony.orm.commit()

        self.open_project(project.get_pk())
