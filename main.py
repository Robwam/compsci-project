#!/usr/bin/env python3

# Maths critical path analysis
# https://revisionworld.com/a2-level-level-revision/maths/decision-maths-0/critical-path-analysis

import math
import sys
from PyQt5.QtWidgets import *

# Events connect activities, starting at the source node and ending at the sink node
class Event():
    def __init__(self, identifier, dependencies, earlyStart=0, lateStart=0):
        self.identifier = identifier
        self.dependencies = dependencies
        self.earlyStart = earlyStart
        self.lateStart = lateStart

    def __repr__(self):
        return "%s [%i|%i]" % (self.identifier, self.earlyStart, self.lateStart) # - %i - %s" % (self.name, self.duration, self.dependencies)

# Activities are tasks that come from an event and lead to an event
class Activity():
    def __init__(self, name, duration, source=None, target=None, floatTime=0):
        self.name = name
        self.duration = duration
        self.source = source
        self.target = target
        self.floatTime = floatTime

    def __repr__(self):
        return "%s (%i)" % (self.name, self.duration)

# Dummies are activities with 0 duration
class DummyActivity(Activity):
    def __init__(self, source, target=None):
        self.name = 'Dummy'
        self.duration = 0
        self.source = source
        self.target = target

# The overarching project that needs to be completed
# Made up of events happening in sequence
class Project():
    def __init__(self, events, activities):
        self.events = events
        self.activities = activities

    # Return a list of activities in which can be done
    def orderEvents(self):
        ordered = []
        eventList = self.events
        while len(eventList) > 0:
            eventAdded = False
            for event in eventList:
                addEvent = True
                for dep in event.dependencies:
                    if dep.source not in ordered:
                        addEvent = False
                        break

                if addEvent:
                    ordered.append(event)
                    eventList.remove(event)
                    eventAdded = True

            if eventAdded == False:
                Exception("Events unorderable")

        self.events = ordered

    def calcEarlyTimes(self):
        for event in self.events:
            maxEarlyStart = 0
            for activity in event.dependencies:
                potentialStart = activity.duration + activity.source.earlyStart
                if potentialStart > maxEarlyStart:
                    maxEarlyStart = potentialStart

            event.earlyStart = maxEarlyStart

    def activitiesFromEvent(self, event):
        out_activities = []
        for activity in self.activities:
            if activity.source == event:
                out_activities.append(activity)

        return out_activities

    def calcLateTimes(self):
        # reversed for backwards pass
        reversedList = list(reversed(self.events))

        #special cases for sink event
        self.events[-1].lateStart = self.events[-1].earlyStart

        for event in reversedList[1:]:
            min_lateStart = math.inf
            for activity in self.activitiesFromEvent(event):
                potentialLateTime = activity.target.lateStart - activity.duration
                if potentialLateTime < min_lateStart:
                    min_lateStart = potentialLateTime

            event.lateStart = min_lateStart

    def calcFloats(self):
        for activity in self.activities:
            activity.floatTime = activity.target.lateStart - activity.duration - activity.source.earlyStart

    def findCriticalActivities(self):
        criticalActivities = []
        for activity in self.activities:
            if activity.floatTime == 0:
                criticalActivities.append(activity)

        self.criticalActivities = criticalActivities
        # these activities are likely out of order and need to be ordered

    # NOTE: This only finds a single criticle path
    # NOTE: This hangs if there is no criticle path
    def criticalPath(self):
        path = []
        nextEvent = self.events[0]
        while (True):
            path.append(nextEvent)

            # Check if this is the sink event, if so break
            if nextEvent == self.events[-1]:
                break

            # Look at all out activities, choose a criticle one
            for activity in self.activitiesFromEvent(nextEvent):
                if activity in self.criticalActivities:
                    nextEvent = activity.target
                    break

        return path

    def workerEstimate(self):
        return None

    def createSchedule(self):
        return None


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
class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.inputData = [] # Rows, each contains sub array for columns
        self.project = None

        self.initUI()


    def initUI(self):
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

        # Right virticle box
        rightVbox = QVBoxLayout()
        rightVbox.addWidget(self.tableWidget)

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

        event_duration = self.event_duration_textbox.text()
        self.event_duration_textbox.setText('')

        event_dependencies = self.event_dependencies_textbox.text()
        self.event_dependencies_textbox.setText('')

        self.inputData.append([event_name, event_duration, event_dependencies])

        # TODO add event to table
        self.updateTable()

    def updateTable(self):
        for r, row in enumerate(self.inputData):
            for c, col in enumerate(row):
                self.tableWidget.setItem(r,c, QTableWidgetItem(col))


    def create_schedule_project(self):
        # TODO
        #   - New project object
        #   - Convert our input data to event Objects & Activity Objects & Dummy objects
        #   - Run criticle path & ouput to console for now

        for row in self.inputData:
            event = Event(row[0])

        #self.project = Project(events, activities)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
