from Scheduler.Views.SchedulePlotCanvas import SchedulePlotCanvas
from Scheduler.Controllers.input_to_project import data_to_events_and_activities
from Scheduler.Models.Project import Project

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui

import pickle

import logging
logger = logging.getLogger('root')

# TODO
DEBUG = True

TEST_DATA = [
    ['A', 3, set()],
    ['B', 5, set()],
    ['C', 2, set(['A'])],
    ['D', 3, set(['A'])],
    ['E', 3, set(['B', 'D'])],
    ['F', 5, set(['C', 'E'])],
    ['G', 1, set(['C'])],
    ['H', 2, set(['F', 'G'])],
]

'''
TODO:
    - Set event dependency list view max size
    - Document functions
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
        self.setWindowTitle('Scheduler')

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
          'data': self.main_widget.get_table_data(),
          'has_been_scheduled': self.main_widget.has_been_scheduled,
          'project_name': self.main_widget.project_name_textbox.text(),
          'worker_count': self.main_widget.project_worker_count_textbox.text()
        }

        pickle.dump(data, open(path, "wb"))

    def load_project(self):
        path, _ = QFileDialog.getOpenFileName(self, "Load Project", "","All Files (*.sched)")

        # No action if cancel
        if not path:
            return

        data = pickle.load(open(path, "rb"))

        # TODO clear the table
        self.main_widget.table_widget.setRowCount(0)

        # Load data into table
        for row in data['data']:
            row[2] = ','.join(row[2])
            self.main_widget.add_event_table_row(row)

        if data['project_name']:
            self.main_widget.project_name_textbox.setText(data['project_name'])

        if data['worker_count']:
            self.main_widget.project_worker_count_textbox.setText(data['worker_count'])

        if data['has_been_scheduled']:
            self.main_widget.create_schedule_project()

class MainController(QWidget):

    def __init__(self, parent=None):
        super(MainController, self).__init__(parent)

        self.event_names = []
        self.project = None
        self.graph = None
        self.has_been_scheduled = False

        self.init_ui()

        # TODO NOTE debuggin prepopulate with test data
        if DEBUG:
            for row, item in enumerate(TEST_DATA):
                self.event_name_textbox.setText(item[0])
                self.event_duration_textbox.setText(str(item[1]))
                self.add_event_from_inputs()

                self.add_event_table_row([item[0], item[1], ','.join(item[2])], row_overide=row)
                # TODO NOTE we are not setting the dependency


    def update_dependeny_listview(self):
        listview_model = QtGui.QStandardItemModel()

        for i, event_name in enumerate(self.event_names):
            item = QtGui.QStandardItem(event_name)
            item.setCheckable(True)
            listview_model.appendRow(item)

        self.event_dependency_listview.setModel(listview_model)

    def init_ui(self):
        self.main_widget = QWidget(self)
        add_event_button = QPushButton("Add event")
        add_event_button.clicked.connect(self.add_event_from_inputs)

        schedule_button = QPushButton("Schedule")
        schedule_button.clicked.connect(self.create_schedule_project)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(['Name', 'Duration', 'Dependencies'])

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

        # TODO Testing
        self.event_dependency_listview = QListView(self)
        self.update_dependeny_listview()

        # -- Event Inputs
        # Create our vertical container
        event_inputs_v_box = QVBoxLayout()

        # Create our text boxes
        self.event_name_textbox = QLineEdit(self)
        self.event_duration_textbox = QLineEdit(self)
        self.event_dependencies_textbox = QLineEdit(self)

        # Create 3 horizontal containers
        event_name_h_box = QHBoxLayout()
        event_duration_h_box = QHBoxLayout()
        event_dependencies_h_box = QHBoxLayout()

        # Add our horizontal containers
        event_inputs_v_box.addLayout(event_name_h_box)
        event_inputs_v_box.addLayout(event_duration_h_box)
        event_inputs_v_box.addLayout(event_dependencies_h_box)

        # Create labels and inputs
        # Whitespace is to make all widgets line up
        event_name_h_box.addWidget(QLabel("Name:              "))
        event_name_h_box.addWidget(self.event_name_textbox)

        event_duration_h_box.addWidget(QLabel("Duration:         "))
        event_duration_h_box.addWidget(self.event_duration_textbox)

        event_dependencies_h_box.addWidget(QLabel("Dependencies:"))
        event_dependencies_h_box.addWidget(self.event_dependency_listview)

        # -- Project controls
        project_controls_v_box = QVBoxLayout()
        project_controls_v_box.addLayout(project_metadata_h_box)
        project_controls_v_box.addLayout(event_inputs_v_box)
        project_controls_v_box.addWidget(add_event_button)
        project_controls_v_box.addWidget(schedule_button)

        self.v_box_table_widget = QVBoxLayout()
        self.v_box_table_widget.addWidget(self.table_widget)
        
        # Main hbox
        self.hbox = QHBoxLayout()
        self.hbox.addLayout(project_controls_v_box)
        self.hbox.addLayout(self.v_box_table_widget)

        self.setLayout(self.hbox)

    def get_event_dependencies(self):
        event_dependencies = []
        model = self.event_dependency_listview.model()
        for row in range(model.rowCount()):
            item = model.item(row)
            if item.checkState() == QtCore.Qt.Checked:
                event_dependencies.append(model.data(model.index(row, 0)))

        return event_dependencies

    def add_event_from_inputs(self):
        event_name = self.event_name_textbox.text()
        self.event_name_textbox.setText('')

        # TODO verify this is an interger
        event_duration = int(self.event_duration_textbox.text())
        self.event_duration_textbox.setText('')

        # Add to table
        self.add_event_table_row([event_name, event_duration, ','.join(self.get_event_dependencies())])

        self.update_dependeny_listview()

    def add_event_table_row(self, data, row_overide=None):
        if row_overide is None:
            last_row = self.table_widget.rowCount()
            self.table_widget.setRowCount(last_row+1)
        else:
            last_row = row_overide

        # Update our dependencies and ensure unique
        # TODO order this
        # TODO when table updated this list should be updated, need to add event handler for table change
        if data[0] not in self.event_names:
            self.event_names.append(data[0])

        for i, d in enumerate(data):
            self.table_widget.setItem(last_row, i, QTableWidgetItem(str(d)))

    def get_table_data(self):
        table_model = self.table_widget.model()
        table_data = []
        for row in range(table_model.rowCount()):
            table_data.append([])
            for column in range(table_model.columnCount()):
                index = table_model.index(row, column)
                data = str(table_model.data(index))
                if column == 1:
                    data = int(data)

                if column == 2:
                    data = list(filter(None, data.split(','))) # Remove empty

                table_data[row].append(data)

        return table_data

    def create_schedule_project(self):
        print(self.get_table_data())
        events, activities = data_to_events_and_activities(self.get_table_data())

        # Delete old widget
        if self.graph:
            self.v_box_table_widget.removeWidget(self.graph)
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
        self.v_box_table_widget.addWidget(self.graph)
        self.update()

        self.has_been_scheduled = True
