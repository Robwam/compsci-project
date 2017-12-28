from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui

from Scheduler.Controllers.ProjectWidget import ProjectWidget

import pickle

'''
Project window controller

Adds menu options and shows project widget
'''
class ProjectWindow(QMainWindow):
    def __init__(self, parent=None, project_id=None):
        super(ProjectWindow, self).__init__(parent)

        self.statusBar()

        # Add menu bar options
        menu = self.menuBar().addMenu('File')

        save_project_action = menu.addAction('Save Project')
        save_project_action.triggered.connect(self.save_project)

        load_project_action = menu.addAction('Load Project')
        load_project_action.triggered.connect(self.load_project)

        schedule_image_action = menu.addAction('Save Schedule Image')
        schedule_image_action.triggered.connect(self.save_schedule_image)

        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Project')

        # Add main project widget
        self.main_widget = ProjectWidget(self, project_id=project_id)
        self.setCentralWidget(self.main_widget)

        self.show()

    '''
    Handle close window event

    Args:
        Object evnt: close event object

    Closes the window and refreshes project list (as project name may have changed)
    '''
    def closeEvent(self, evnt):
        self.parent().populate_projects() # Refresh list
        super(ProjectWindow, self).closeEvent(evnt)

    '''
    Handle save schedule image event

    Checks if schedule has been created, opens save dialog
    '''
    def save_schedule_image(self):
        # Error if no schedule diagram
        if not self.main_widget.has_been_scheduled:
            QMessageBox.about(self, "Error", "Please schedule before attempting to save")
            return

        path, _ = QFileDialog.getSaveFileName(self, "Save Schedule Image", "","All Files (*.png)")

        # No action if cancel
        if not path:
            return

        self.main_widget.graph.save_figure(path)

    '''
    Handle save project event

    Opens save dialog, serialises data
    '''
    def save_project(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Project", "","All Files (*.sched)")

        # No action if cancel
        if not path:
            return

        data = {
          'data': self.main_widget.get_table_data(),
          'has_been_scheduled': self.main_widget.has_been_scheduled,
          'project_name': self.main_widget.project_name_textbox.text(),
          'worker_count': self.main_widget.project_worker_count_textbox.text()
        }

        pickle.dump(data, open(path, "wb"))

    '''
    Handle load project event

    Opens load dialog, unserialises data, loads into window
    '''
    def load_project(self):
        path, _ = QFileDialog.getOpenFileName(self, "Load Project", "","All Files (*.sched)")

        # No action if cancel
        if not path:
            return

        data = pickle.load(open(path, "rb"))

        # Clear the table
        self.main_widget.table_widget.setRowCount(0)

        # Load data into table
        for row in data['data']:
            row[2] = ','.join(row[2])
            self.main_widget.add_event_table_row(row)

        if data['project_name']:
            self.main_widget.project_name_textbox.setText(data['project_name'])

        if data['worker_count']:
            self.main_widget.project_worker_count_textbox.setText(data['worker_count'])

        if data['has_been_scheduled']:
            self.main_widget.create_schedule_project()
