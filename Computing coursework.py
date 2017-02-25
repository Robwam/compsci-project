#!/usr/bin/env python3

class Event():
    def __init__(self, name, duration, dependencies, earlyStart=0, lateStart=0):
        self.name = name
        self.duration = duration
        self.dependencies = dependencies
        self.earlyStart = earlyStart
        self.lateStart = lateStart

    def __repr__(self):
        return "%s" % self.name# - %i - %s" % (self.name, self.duration, self.dependencies)


class Project():
    def __init__(self, eventList):
        self.eventList = list(eventList)
        self.orderEvents()

    # Returns a list of events in dependency order
    #
    # For every event which has dependencies in ordered, add this event to ordered
    # If no dependencies are in ordered, go to next event
    # If list is unorderable, raise an exception
    def orderEvents(self):
        ordered = []
        while len(self.eventList) > 0:
            eventAdded = False
            for event in self.eventList:
                addEvent = True
                for dep in event.dependencies:
                    if dep not in ordered:
                        addEvent = False
                        break
                if addEvent:
                    ordered.append(event)
                    self.eventList.remove(event)
                    eventAdded = True

            if eventAdded == False:
                Exception("Events unorderable")

        self.eventList = ordered
        return ordered


    def calcEarlyTime():
        None

    def calcLateTime():
        None

    def calcFloats():
        None

    def criticalActivities():
        #Returns a list of the critical activities
        None

    def criticalPath():
        #Returns the order of events in the critical path
        None

    def workerEstimate():
        #estimate the number of workers required to complete the task in a given
        # timeframe
        None

    def createSchedule():
        None

rmWall = Event('Remove old wall',20, [])
sWall = Event('sand wall', 30, [rmWall])
wpWall = Event('Wallpaper wall', 10, [sWall,rmWall])
lWall = Event('look at wall',40, [wpWall])

P1 = Project([rmWall,wpWall,lWall,sWall])
print(P1.eventList)
