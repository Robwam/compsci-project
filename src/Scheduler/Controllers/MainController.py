from Scheduler.Views.SchedulePlotCanvas import SchedulePlotCanvas
from Scheduler.Controllers.input_to_project import data_to_events_and_activities
from Scheduler.Models.Project import Project

from PyQt5.QtWidgets import *


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
class MainController(QWidget):

    def __init__(self):
        super().__init__()

        self.inputData = [] # Rows, each contains sub array for columns
        self.project = None

        # TODO NOTE debuggin prepopulate with test data
        if DEBUG:
          self.inputData = TEST_DATA

        self.initUI()


    def initUI(self):
        self.main_widget = QWidget(self)
        add_event_button = QPushButton("Add event")
        add_event_button.clicked.connect(self.get_event_input)

        schedule_button = QPushButton("Schedule")
        schedule_button.clicked.connect(self.create_schedule_project)

        #self.le = QLineEdit(self)
        #self.le.move(130, 22)

        self.event_name_textbox = QLineEdit(self)
        self.event_duration_textbox = QLineEdit(self)
        self.event_dependencies_textbox = QLineEdit(self)

        self.tableWidget = QTableWidget()
        self.tableWidget.move(100,100)
        self.tableWidget.setRowCount(10)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(['Name', 'Duration', 'Dependencies'])

        self.updateTable()

        # Left virticle box
        labelsVbox = QVBoxLayout()
        inputsVbox = QVBoxLayout()
        labelsVbox.addWidget(QLabel("Name:"))
        inputsVbox.addWidget(self.event_name_textbox)
        labelsVbox.addWidget(QLabel("Duration:"))
        inputsVbox.addWidget(self.event_duration_textbox)
        labelsVbox.addWidget(QLabel("Dependencies:")) # TODO this should be a dropdown list (checkbox list) of Dependencies
        inputsVbox.addWidget(self.event_dependencies_textbox)

        leftVboxHbox = QHBoxLayout()
        leftVboxHbox.addLayout(labelsVbox)
        leftVboxHbox.addLayout(inputsVbox)


        leftVbox = QVBoxLayout()
        leftVbox.addLayout(leftVboxHbox)
        leftVbox.addWidget(add_event_button)
        leftVbox.addWidget(schedule_button)

        # TODO setup correct graph
        graph = SchedulePlotCanvas(self.main_widget, width=5, height=4, dpi=100)

        # Right virticle box
        rightVbox = QVBoxLayout()
        rightVbox.addWidget(self.tableWidget)
        rightVbox.addWidget(graph)

        hbox = QHBoxLayout()
        hbox.addLayout(leftVbox)
        hbox.addLayout(rightVbox)

        self.setLayout(hbox)

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Buttons')
        self.show()

    def get_event_input(self):
        event_name = self.event_name_textbox.text()
        self.event_name_textbox.setText('')

        # TODO verify this is an interger
        event_duration = int(self.event_duration_textbox.text())
        self.event_duration_textbox.setText('')

        event_dependencies = self.event_dependencies_textbox.text()
        self.event_dependencies_textbox.setText('')

        self.inputData.append([event_name, event_duration, event_dependencies])

        # TODO add event to table
        self.updateTable()

    def updateTable(self):
        for r, row in enumerate(self.inputData):
            for c, col in enumerate(row):
                self.tableWidget.setItem(r,c, QTableWidgetItem(str(col)))


    def create_schedule_project(self):
        # TODO
        #   - New project object
        #   - Convert our input data to event Objects & Activity Objects & Dummy objects
        #   - Run criticle path & ouput to console for now

        events, activities = data_to_events_and_activities(self.inputData)

        self.project = Project(events, activities)
        print(self.project.createSchedule())
