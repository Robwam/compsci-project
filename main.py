#!/usr/bin/env python3

# Maths critical path analysis
# https://revisionworld.com/a2-level-level-revision/maths/decision-maths-0/critical-path-analysis

import math
import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem

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
        for activity in self.activities.values():
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
        for activity in self.activities.values():
            activity.floatTime = activity.target.lateStart - activity.duration - activity.source.earlyStart

    def findCriticalActivities(self):
        criticalActivities = []
        for activity in self.activities.values():
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


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        self.setGeometry(300, 300, 290, 150)

        # Button stuff
        btn1 = QPushButton("Button 1", self)
        btn1.move(30, 50)

        btn2 = QPushButton("Button 2", self)
        btn2.move(150, 50)

        btn1.clicked.connect(self.buttonClicked)
        btn2.clicked.connect(self.buttonClicked)


        # Table stuff
        self.tableWidget = QTableWidget()
        self.tableWidget.move(100,100)
        self.tableWidget.setRowCount(10)
        self.tableWidget.setColumnCount(2)

        self.tableWidget.setItem(1,1, QTableWidgetItem("TEXT")

        # Set out layout + add table
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

        # Other stuff
        self.statusBar()

        self.setWindowTitle('Event sender')
        self.show()


    def buttonClicked(self):

        sender = self.sender()
        self.statusBar().showMessage(sender.text() + ' was pressed')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
