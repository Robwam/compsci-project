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
        for event in self.ordered:
            maxEarlyStart = 0
            for dep in event.dependencies:
                if dep.duration > maxEarlyStart:
                    maxEarlyStart = dep.duration

            event.earlyStart = maxEarlyStart

    def calcLateTime(self):
        #unsure if this works
        reverseOrdered = list(reversed(ordered))
        for event in reverseOrdered:
            minLateStart = reverseOrdered[0].duration
            for dep in event.dependencies:
                if dep.duration < minLateStart:
                    minLateStart = dep.duration

            event.lateStart = minLateStart

    def calcFloats(self):
        return None

    def criticalActivities(self):
        #Returns a list of the critical activities
        return None

    def criticalPath(self):
        #Returns the order of events in the critical path
        return None

    def workerEstimate(self):
        #estimate the number of workers required to complete the task in a given
        # timeframe
        return None

    def createSchedule(self):
        return None

rmWall = Event('Remove old wall',20, [])
sWall = Event('sand wall', 30, [rmWall])
wpWall = Event('Wallpaper wall', 10, [sWall,rmWall])
lWall = Event('look at wall',40, [wpWall])

P1 = Project([rmWall,wpWall,lWall,sWall])
print(P1.eventList)
