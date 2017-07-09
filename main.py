#!/usr/bin/env python3

# Maths critical path analysis
# https://revisionworld.com/a2-level-level-revision/maths/decision-maths-0/critical-path-analysis

import plot_ghantt

import math
import sys
from PyQt5.QtWidgets import *

import matplotlib
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

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

def data_to_events_and_activities(data):
    # Convert csv dependencies into list
    # NOTE we sort dependencies so they are order indepenent
    for row in data:
        if row[2] == '': # If no dependencies, add empty list
            row.append([])
        else:
            row.append(sorted(row[2].split(',')))
            row[2] = ','.join(row[3])

    # Create Events
    unique_dependencies = {}
    for row in data:
        if row[2] not in unique_dependencies and row[3] != []:
            unique_dependencies[row[2]] = row[3]

    events = {
        'source': Event('source', []),
        'sink': Event('sink', [])
    }

    for dependencies in unique_dependencies:
        events[dependencies] = Event(dependencies, [])

    # Create activities and update their source events
    activities = {}
    for row in data:
        if row[3] == []:
            source = events['source']
        else:
            source = events[row[2]]

        activities[row[0]] = Activity(row[0], row[1], source, None)

    dummies = {}

    # Update the activities target events
    for activity_key, activity in activities.items():
        potential_targets = list(filter(lambda s: activity_key in s, unique_dependencies))
        if len(potential_targets) == 0:
            activity.target = events['sink']
            events['sink'].dependencies.append(activity)
        elif len(potential_targets) == 1:
            activity.target = events[potential_targets[0]]
        elif len(potential_targets) == 2: # TODO More cases
            if (potential_targets[0] == activity_key):
                i, j = [0, 1]
            elif (potential_targets[1] == activity_key):
                i, j = [1, 0]
            else:
                print('We need a dummy! Not covered', activity_key, potential_targets)
                continue

            activity.target = events[potential_targets[i]]
            dummies[activity_key + '_dummy'] = DummyActivity(activity_key + '_dummy', events[potential_targets[i]], events[potential_targets[j]])
            e = events[potential_targets[j]]
            e.dependencies.append(dummies[activity_key + '_dummy'])
        else:
            print('We need a dummy!', activity_key, potential_targets)

    # Merge dummies with real
    activities = {**activities, **dummies}

    # Link events & activities
    for event in events.values():

        for dep in event.identifier.split(','):
            if dep in ['source', 'sink']: # TODO check dis
                continue
            if dep + '_dummy' in [s.name for s in event.dependencies]:
                continue
            event.dependencies.append(activities[dep])

    return [list(events.values()), list(activities.values())]

# Events connect activities, starting at the source node and ending at the sink node
class Event():
    def __init__(self, identifier, dependencies, earlyStart=0, lateStart=0):
        self.identifier = identifier
        self.dependencies = dependencies
        self.earlyStart = earlyStart
        self.lateStart = lateStart

    def __repr__(self):
        if self.earlyStart == math.inf:
            early_start = 'inf'
        else:
            early_start = str(self.earlyStart)

        if self.lateStart == math.inf:
            lateStart = 'inf'
        else:
            lateStart = str(self.lateStart)

        return "%s [%s|%s, [%s]]" % (self.identifier, early_start, lateStart, ','.join([d.name for d in self.dependencies])) # - %i - %s" % (self.name, self.duration, self.dependencies)

# Activities are tasks that come from an event and lead to an event
class Activity():
    def __init__(self, name, duration, source=None, target=None, floatTime=0):
        self.name = name
        self.duration = duration
        self.source = source
        self.target = target
        self.floatTime = floatTime

    def __repr__(self):
        if (self.source and self.target):
            return "%s [%i, %s->%s]" % (self.name, self.duration, self.source.identifier, self.target.identifier)
        else:
            return "%s [%i]" % (self.name, self.duration)

# Dummies are activities with 0 duration
class DummyActivity(Activity):
    def __init__(self, name, source, target=None):
        self.name = name
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
        events_path = []
        activities_path = []
        nextEvent = self.events[0]
        events_path.append(nextEvent)
        last = False
        while (not last):


            # Check if this is the sink event, if so break
            if nextEvent == self.events[-1]:
                last = True

            # Look at all out activities, choose a criticle one
            for activity in self.activitiesFromEvent(nextEvent):
                if activity in self.criticalActivities:
                    activities_path.append(activity)
                    nextEvent = activity.target
                    break

            events_path.append(nextEvent)

        for activity in self.activitiesFromEvent(nextEvent):
            if activity in self.criticalActivities:
                activities_path.append(activity)

        self.critcle_activities_path = activities_path
        self.critcle_events_path = events_path
        self.criticle_path_length = sum([a.duration for a in self.critcle_activities_path])

    def calc_min_num_worker(self):
        total_time = sum([a.duration for a in self.activities])
        return math.ceil(total_time / self.criticle_path_length)

    def calc_schedule(self):
        pass

    def naive_schedule(self, num_workers):
        jobs = self.events

        workers_jobs = {}

        for worker in range(0, num_workers):
            workers_jobs[worker] = []

        while len(jobs) > 0:
            for worker in workers_jobs:
                if len(jobs) > 0:
                    workers_jobs[worker].append(jobs.pop())
                else:
                    break

        return workers_jobs

    def createSchedule(self):
        self.orderEvents()
        self.calcEarlyTimes()
        self.calcLateTimes()
        self.calcFloats()
        self.findCriticalActivities()
        self.criticalPath()

        workers = self.calc_min_num_worker()

        return self.naive_schedule(workers)


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

        # NOTE debuggin prepopulate with test data
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
        graph = MyMplCanvas(self.main_widget, width=5, height=4, dpi=100)

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

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
      # TODO this is test data, should be real, duh
      ylabels, effort, task_dates, pos = plot_ghantt.test_data()
      plot_ghantt.plot_ghantt(self.fig, self.axes, ylabels, effort, task_dates, pos)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
