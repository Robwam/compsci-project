from Scheduler.Views.SchedulePlotCanvas import SchedulePlotCanvas
from Scheduler.Controllers.input_to_project import data_to_events_and_activities

from Scheduler.Models.Project import Project
from Scheduler.Services.ScheduleService import ScheduleService

from Scheduler.Exceptions import ScheduleError

import pony.orm

from functools import partial

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui

# TODO
# TEST_DATA = [
#     ['A', 3, set()],
#     ['B', 5, set()],
#     ['C', 2, set(['A'])],
#     ['D', 3, set(['A'])],
#     ['E', 3, set(['B', 'D'])],
#     ['F', 5, set(['C', 'E'])],
#     ['G', 1, set(['C'])],
#     ['H', 2, set(['F', 'G'])],
# ]

class ProjectWidget(QWidget):

    def __init__(self, parent=None, project_id=None):
        super(ProjectWidget, self).__init__(parent)

        self.project_id = project_id

        self.event_names = []
        self.graph = None
        self.has_been_scheduled = False

        self.init_ui()
        self.load_from_db()

        # # TODO NOTE debuggin prepopulate with test data
        # if DEBUG:
        #     for row, item in enumerate(TEST_DATA):
        #         self.event_name_textbox.setText(item[0])
        #         self.event_duration_textbox.setText(str(item[1]))
        #         self.add_event_from_inputs()
        #
        #         self.add_event_table_row([item[0], item[1], ','.join(item[2])], row_overide=row)
        #         # TODO NOTE we are not setting the dependency

    @pony.orm.db_session
    def load_from_db(self):
        project = Project.get(id=self.project_id)
        self.project_name_textbox.setText(project.name)

        if project.number_of_workers:
            self.project_worker_count_textbox.setText(str(project.number_of_workers))

        # Only continue if there are events
        if project.events is None or len(project.events) == 0:
            return

        events = ScheduleService.order_events(project.events)
        activities = ScheduleService.order_activities(events)

        activities = reversed(activities)

        for row, activity in enumerate(activities):
            self.event_name_textbox.setText(activity.name)
            self.event_duration_textbox.setText(str(activity.duration))
            self.add_event_from_inputs()

            dependencies = [a.name for a in activity.source.dependencies]
            self.add_event_table_row([activity.name, str(activity.duration), ','.join(dependencies)], row_overide=row)

            #self.add_event_table_row([item[0], item[1], ','.join(item[2])], row_overide=row)
            # TODO NOTE we are not setting the dependency

        if project.has_been_scheduled:
            self.create_schedule_project()

    @pony.orm.db_session
    def update_project_db(self):
        project = Project.get(id=self.project_id)
        project.name = self.project_name_textbox.text()

         # TODO validation
        if self.project_worker_count_textbox.text():
            project.number_of_workers = int(self.project_worker_count_textbox.text())

    def update_dependeny_listview(self):
        listview_model = QtGui.QStandardItemModel()

        for i, event_name in enumerate(self.event_names):
            item = QtGui.QStandardItem(event_name)
            item.setCheckable(True)
            listview_model.appendRow(item)

        self.event_dependency_listview.setModel(listview_model)

    def init_ui(self):
        self.main_widget = QWidget(self)
        add_event_button = QPushButton("Add activity")
        add_event_button.clicked.connect(self.add_event_from_inputs)
        add_event_button.setToolTip('Add a new activity to the project')

        schedule_button = QPushButton("Schedule")
        schedule_button.clicked.connect(self.create_schedule_project)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(['Name', 'Duration', 'Dependencies', 'Delete'])
        self.table_widget.setSelectionMode(QTableWidget.NoSelection)

        # Fix headers
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(0, header.ResizeToContents)
        header.setSectionResizeMode(1, header.ResizeToContents)
        header.setSectionResizeMode(2, header.Stretch)
        header.setSectionResizeMode(3, header.ResizeToContents)

        # -- Project Metadata
        # Create our Horizontal container
        project_metadata_h_box = QHBoxLayout()

        # Create our text boxes
        self.project_name_textbox = QLineEdit()
        self.project_name_textbox.textChanged.connect(self.update_project_db)
        self.project_worker_count_textbox = QLineEdit()
        self.project_worker_count_textbox.textChanged.connect(self.update_project_db)

        # Create two vertical layouts for labels and inputs
        project_metadata_labels_v_box = QVBoxLayout()
        project_metadata_inputs_v_box = QVBoxLayout()

        # Add our label and input layouts
        project_metadata_h_box.addLayout(project_metadata_labels_v_box)
        project_metadata_h_box.addLayout(project_metadata_inputs_v_box)

        # Create labels and inputs
        proejct_name_label = QLabel("Project name:")
        proejct_name_label.setToolTip('The name of the project')
        project_metadata_labels_v_box.addWidget(proejct_name_label)
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
        self.event_name_textbox = QLineEdit()
        self.event_duration_textbox = QLineEdit()
        self.event_dependencies_textbox = QLineEdit()

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

        # TODO check atleast one event added before schedule created

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
        event_duration = self.event_duration_textbox.text()

        if not self.validate_activity(event_name, event_duration):
            return

        self.event_name_textbox.setText('')
        self.event_duration_textbox.setText('')
        self.add_event_table_row([event_name, event_duration, ','.join(self.get_event_dependencies())])
        self.update_dependeny_listview()

    def show_error(self, message):
        QMessageBox.about(self, "Error", message)

    def validate_activity(self, event_name, event_duration):
        if not event_duration.isdigit():
            self.show_error("Duration must be an integer")
            return False
        elif event_name in self.event_names:
            self.show_error("Activity name is not unique")
            return False
        elif event_name == '':
            self.show_error("Activity name cannot be empty")
            return False

        return True

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

        # Add the delete button
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(partial(self.delete_activity, data[0], last_row))

        self.table_widget.setCellWidget(last_row, 3, delete_button)

    def delete_activity(self, activity_name, row_index):
        self.table_widget.removeRow(row_index)

        activity_index = self.event_names.index(activity_name)
        del(self.event_names[activity_index])
        self.update_dependeny_listview()

        # Delete any dependencies
        for row_index, row in enumerate(self.get_table_data()):
            dependencies = row[2]
            if activity_name in dependencies:
                del(dependencies[dependencies.index(activity_name)])
                self.table_widget.setItem(row_index, 2, QTableWidgetItem(",".join(dependencies)))


    def get_table_data(self):
        table_model = self.table_widget.model()
        table_data = []

        for row in range(table_model.rowCount()):
            table_data.append([])

            # TODO as delete is in the last index
            for column in range(table_model.columnCount() - 1):
                index = table_model.index(row, column)
                data = str(table_model.data(index))
                if column == 1:
                    data = int(data)

                if column == 2:
                    data = list(filter(None, data.split(','))) # Remove empty

                table_data[row].append(data)

        return table_data

    def create_schedule_project(self):
        # Delete old widget
        if self.graph:
            self.v_box_table_widget.removeWidget(self.graph)
            self.graph.deleteLater()

        # Get worker count
        worker_count_str = self.project_worker_count_textbox.text()
        if len(worker_count_str) == 0:
            worker_count = None
        elif worker_count_str.isdigit() and int(worker_count_str) > 0:
            worker_count = int(worker_count_str)
        else:
            self.show_error("Worker count must be a positive integer")
            return

        with pony.orm.db_session:
            project = Project.get(id=self.project_id)
            for event in project.events:
                event.delete()
            data_to_events_and_activities(self.get_table_data(), project)

            try:
                schedule = ScheduleService.create_schedule(events=project.events, num_of_workers=worker_count)
            except ScheduleError as err:
                self.show_error(str(err))
                return

            project.has_been_scheduled = True

        self.graph = SchedulePlotCanvas(self.main_widget, width=5, height=4, dpi=100, data=schedule)
        self.v_box_table_widget.addWidget(self.graph)
        self.update()

        # NOTE we save the databse only on update of schedule
        self.update_project_db()
