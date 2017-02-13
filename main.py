#!/usr/bin/env python3

# this is my computing project prototype

class Project():
    def __init__(self, events, startTime=0):
        self.events = events
        self.starTime = startTime

    # Returns a ordered list of evetns or None if not possible
    def eventOrder(self):
        ordered = []
        events = list(self.events)

        # TODO infinite loop if dependencies wrong
        while len(events) > 0:
            itemChanged = False
            for event in events:
                shouldAdd = True
                for dep in event.dependencies:
                    if dep not in ordered:
                        shouldAdd = False
                        break
                if shouldAdd:
                    itemChanged = True
                    ordered.append(event)
                    events.remove(event)

            if not itemChanged:
                return None # Events cannot be ordered

        return ordered

    # Updates events earliest & latest start times
    def calcEarlyTimes(self):
        ordered = self.eventOrder()
        for event in ordered:
            maxEarlyStart = 0
            for dep in event.dependencies:
                if dep.earlyStart > maxEarlyStart:
                    maxEarlyStart = dep.earlyStart

            event.earlyStart = maxEarlyStart

class Event():
    def __init__(self, name, duration, dependencies, earlyStart=None, lateStart=None):
        self.name = name
        self.duration = duration
        self.dependencies = dependencies
        self.earlyStart = earlyStart
        self.lateStart = lateStart

    def __repr__(self):
        return "%s" % self.name# - %i - %s" % (self.name, self.duration, self.dependencies)

e1 = Event('e1', 2, [])
e3 = Event('e3',4,[e1])
e2 = Event('e2', 3, [e1,e3])
e4 = Event('e4',4,[e2])
e5 = Event('e5', 3, [e4])

events = [e1, e2, e3, e4, e5]

p1 = Project(events)
print(p1.eventOrder())
p1.calcEarlyTimes()
print(e1.earlyStart)
print(e2.earlyStart)
print(e3.earlyStart)
print(e4.earlyStart)
print(e5.earlyStart)
