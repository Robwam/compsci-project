#!/usr/bin/env python3

# Maths critical path analysis
# https://revisionworld.com/a2-level-level-revision/maths/decision-maths-0/critical-path-analysis


class Event():
    def __init__(self, identifier, dependencies, earlyStart=0, lateStart=0):
        self.identifier = identifier
        self.dependencies = dependencies
        self.earlyStart = earlyStart
        self.lateStart = lateStart

    def __repr__(self):
        return "%s [%i|%i]" % (self.identifier, self.earlyStart, self.lateStart) # - %i - %s" % (self.name, self.duration, self.dependencies)

class Activity():
    def __init__(self, name, duration, source=None, target=None):
        self.name = name
        self.duration = duration
        self.source = source
        self.target = target

    def __repr__(self):
        return "%s (%i)" % (self.name, self.duration)

class DummyActivity(Activity):
    def __init__(self, source, target=None):
        self.name = 'Dummy'
        self.duration = 0
        self.source = source
        self.target = target


class Project():
    def __init__(self, events):
        self.events = events

    # Return a list of activites in which can be done
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

    #
    #
    # def calcEarlyTime(self):
    #     for event in self.eventList:
    #         maxEarlyStart = 0
    #         for dep in event.dependencies:
    #             potentialSTime = dep.earlyStart + event.duration
    #             if potentialSTime > maxEarlyStart:
    #                 maxEarlyStart = potentialSTime
    #
    #         event.earlyStart = maxEarlyStart
    #
    # def calcLateTime(self):
    #     #unsure if this works
    #     reversedEventList = list(reversed(self.eventList))
    #     previousEvent = None
    #     for event in reversedEventList:
    #
    #
    #
    #         # minLateStart = reverseOrdered[0].duration
    #         # for dep in event.dependencies:
    #         #     if dep.duration < minLateStart:
    #         #         minLateStart = dep.duration
    #         #
    #         # event.lateStart = minLateStart
    #         previousEvent = event
    #
    # def calcFloats(self):
    #     return None
    #
    # def criticalActivities(self):
    #     #Returns a list of the critical activities
    #     return None
    #
    # def criticalPath(self):
    #     #Returns the order of events in the critical path
    #     return None
    #
    # def workerEstimate(self):
    #     #estimate the number of workers required to complete the task in a given
    #     # timeframe
    #     return None
    #
    # def createSchedule(self):
    #     return None




activites = {
    'A': Activity('A', 3),
    'B': Activity('B', 5),
    'C': Activity('C', 2),
    'D': Activity('D', 3),
    'E': Activity('E', 3),
    'F': Activity('F', 5),
    'G': Activity('G', 1),
    'H': Activity('H', 2),
}

event_0 = Event(0, [])
event_1 = Event(1, [ activites['A'] ])
event_2 = Event(2, [ activites['B'], activites['D'] ])
event_3 = Event(3, [ activites['C'] ])

dummy_34 = DummyActivity(event_3)

event_4 = Event(4, [ activites['E'], dummy_34])
event_5 = Event(5, [ activites['F'],  activites['G'] ])
event_6 = Event(6, [ activites['H'] ])

activites['A'].source = event_0
activites['A'].target = event_1

# TODO add source and target events for activites
# Do this for all the other activites


P1 = Project([event_0, event_1, event_2, event_3, event_4, event_5, event_6])
