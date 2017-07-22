from Scheduler.Views.SchedulePlotCanvas import SchedulePlotCanvas
from Scheduler.Controllers.input_to_project import data_to_events_and_activities
from Scheduler.Models.Project import Project

from PyQt5.QtWidgets import *

import pickle

import logging
logger = logging.getLogger('root')

# TODO
DEBUG = True

TEST_DATA = [
    ['A', 3, ''],
    ['B', 5, ''],
    ['C', 2, 'A'],
    ['D', 3, 'A'],
    ['E', 3, 'B,D'],
    ['F', 5, 'C,E'],
    ['G', 1, 'C'],
    ['H', 2, 'F,G'],
]

'''
TODO:
    - Allow deletion of events
    - Dropdown checkbox list to add dependencies
    - Make sure activity names are unique
    - Auto space table on window resize
    - Create project screen
        - Project name
        - Start date
        - End date (5/7 days away from start)
        - Load project
    - Save project
'''

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.statusBar()

        menu = self.menuBar().addMenu('File')

        save_project_action = menu.addAction('Save Project')
        save_project_action.triggered.connect(self.save_project)

        load_project_action = menu.addAction('Load Project')
        load_project_action.triggered.connect(self.load_project)

        schedule_image_action = menu.addAction('Save Schedule Image')
        schedule_image_action.triggered.connect(self.save_schedule_image)

        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Buttons')

        self.main_widget = MainController(self)
        self.setCentralWidget(self.main_widget)
        self.show()

    def save_schedule_image(self):
        # Error if no schedule diagram
        if not self.main_widget.has_been_scheduled:
            QMessageBox.about(self, "Error", "Please schedule before attempting to save")
            return

        path, _ = QFileDialog.getSaveFileName(self, "Save Schedule Image", "","All Files (*.png)")

        # No action if cancel
        if not path:
            return

        self.main_widget.graph.save_figure(path)

    def save_project(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Project", "","All Files (*.sched)")

        # No action if cancel
        if not path:
            return

        data = {
          'data': self.main_widget.event_input_data,
          'has_been_scheduled': self.main_widget.has_been_scheduled
        }

        pickle.dump(data, open(path, "wb"))

    def load_project(self):
        path, _ = QFileDialog.getOpenFileName(self, "Load Project", "","All Files (*.sched)")

        # No action if cancel
        if not path:
            return

        data = pickle.load(open(path, "rb"))
        self.main_widget.event_input_data = data['data']
        self.main_widget.updateTable()

        if data['has_been_scheduled']:
            self.main_widget.create_schedule_project()

class MainController(QWidget):

    def __init__(self, parent=None):
        super(MainController, self).__init__(parent)

        self.event_input_data = [] # Rows, each contains sub array for columns
        self.project = None
        self.graph = None
        self.has_been_scheduled = False

        # TODO NOTE debuggin prepopulate with test data
        if DEBUG:
          self.event_input_data = TEST_DATA

        self.initUI()


    def initUI(self):
        self.main_widget = QWidget(self)
        add_event_button = QPushButton("Add event")
        add_event_button.clicked.connect(self.get_event_input)

        schedule_button = QPushButton("Schedule")
        schedule_button.clicked.connect(self.create_schedule_project)

        #self.le = QLineEdit(self)
        #self.le.move(130, 22)



        self.tableWidget = QTableWidget()
        self.tableWidget.move(100,100)
        self.tableWidget.setRowCount(10)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(['Name', 'Duration', 'Dependencies'])

        self.updateTable()

        # -- Project Metadata
        # Create our Horizontal container
        project_metadata_h_box = QHBoxLayout()

        # Create our text boxes
        self.project_name_textbox = QLineEdit(self)
        self.project_worker_count_textbox = QLineEdit(self)

        # Create two vertical layouts for labels and inputs
        project_metadata_labels_v_box = QVBoxLayout()
        project_metadata_inputs_v_box = QVBoxLayout()

        # Add our label and input layouts
        project_metadata_h_box.addLayout(project_metadata_labels_v_box)
        project_metadata_h_box.addLayout(project_metadata_inputs_v_box)

        # Create labels and inputs
        project_metadata_labels_v_box.addWidget(QLabel("Project name:"))
        project_metadata_inputs_v_box.addWidget(self.project_name_textbox)
        project_metadata_labels_v_box.addWidget(QLabel("Number of worker:"))
        project_metadata_inputs_v_box.addWidget(self.project_worker_count_textbox)


        # -- Event Inputs
        # Create our Horizontal container
        event_inputs_h_box = QHBoxLayout()

        # Create our text boxes
        self.event_name_textbox = QLineEdit(self)
        self.event_duration_textbox = QLineEdit(self)
        self.event_dependencies_textbox = QLineEdit(self)

        # Create two vertical layouts for labels and inputs
        event_input_labels_v_box = QVBoxLayout()
        event_input_inputs_v_box = QVBoxLayout()

        # Add our label and input layouts
        event_inputs_h_box.addLayout(event_input_labels_v_box)
        event_inputs_h_box.addLayout(event_input_inputs_v_box)
        event_inputs_h_box.addWidget(add_event_button)

        # Create labels and inputs
        event_input_labels_v_box.addWidget(QLabel("Name:"))
        event_input_inputs_v_box.addWidget(self.event_name_textbox)
        event_input_labels_v_box.addWidget(QLabel("Duration:"))
        event_input_inputs_v_box.addWidget(self.event_duration_textbox)
        event_input_labels_v_box.addWidget(QLabel("Dependencies:"))
        event_input_inputs_v_box.addWidget(self.event_dependencies_textbox)

        # -- Project controls
        project_controls_v_box = QVBoxLayout()
        project_controls_v_box.addLayout(project_metadata_h_box)
        project_controls_v_box.addLayout(event_inputs_h_box)
        project_controls_v_box.addWidget(add_event_button)
        project_controls_v_box.addWidget(schedule_button)

        # # Event IO
        # self.event_name_textbox = QLineEdit(self)
        # self.event_duration_textbox = QLineEdit(self)
        # self.event_dependencies_textbox = QLineEdit(self)
        #
        # labelsVbox = QVBoxLayout()
        # inputsVbox = QVBoxLayout()
        # labelsVbox.addWidget(QLabel("Name:"))
        # inputsVbox.addWidget(self.event_name_textbox)
        # labelsVbox.addWidget(QLabel("Duration:"))
        # inputsVbox.addWidget(self.event_duration_textbox)
        # labelsVbox.addWidget(QLabel("Dependencies:")) # TODO this should be a dropdown list (checkbox list) of Dependencies
        # inputsVbox.addWidget(self.event_dependencies_textbox)
        #
        # leftVboxHbox = QHBoxLayout()
        # leftVboxHbox.addLayout(labelsVbox)
        # leftVboxHbox.addLayout(inputsVbox)


        # leftVbox = QVBoxLayout()
        # leftVbox.addLayout(leftVboxHbox)
        # leftVbox.addWidget(project_metadata_h_box)
        # leftVbox.addWidget(add_event_button)
        # leftVbox.addWidget(schedule_button)

        # Right verticle box
        self.rightVbox = QVBoxLayout()
        self.rightVbox.addWidget(self.tableWidget)

        hbox = QHBoxLayout()
        hbox.addLayout(project_controls_v_box)
        hbox.addLayout(self.rightVbox)

        self.setLayout(hbox)


    def get_event_input(self):
        event_name = self.event_name_textbox.text()
        self.event_name_textbox.setText('')

        # TODO verify this is an interger
        event_duration = int(self.event_duration_textbox.text())
        self.event_duration_textbox.setText('')

        event_dependencies = self.event_dependencies_textbox.text()
        self.event_dependencies_textbox.setText('')

        self.event_input_data.append([event_name, event_duration, event_dependencies])

        # TODO add event to table
        self.updateTable()

    def updateTable(self):
        for r, row in enumerate(self.event_input_data):
            for c, col in enumerate(row):
                self.tableWidget.setItem(r,c, QTableWidgetItem(str(col)))


    def create_schedule_project(self):
        events, activities = data_to_events_and_activities(self.event_input_data)

        # Delete old widget
        if self.graph:
            self.rightVbox.removeWidget(self.graph)
            self.graph.deleteLater()

        # Get worker count
        worker_count_str = self.project_worker_count_textbox.text()
        if len(worker_count_str) == 0:
            worker_count = None
        else:
            try:
                worker_count = int(worker_count_str)
                if worker_count <= 0:
                    raise Exception("worker count must be positive")
            except:
                QMessageBox.about(self, "Error", "Worker count must be a positive integer")
                return

        self.project = Project(events, activities)
        schedule = self.project.createSchedule(worker_count)

        self.graph = SchedulePlotCanvas(self.main_widget, width=5, height=4, dpi=100, data=schedule)
        self.rightVbox.addWidget(self.graph)
        self.update()

        self.has_been_scheduled = True
