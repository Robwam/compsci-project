#!/usr/bin/env python3

# Maths critical path analysis
# https://revisionworld.com/a2-level-level-revision/maths/decision-maths-0/critical-path-analysis

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
    def __init__(self, events):
        self.events = events

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
            
    def calcLateTimes(self):
        reversedList = list(reversed(self.events))
        
        #special cases for source and sink events
        self.events[0].lateStart = 0
        self.events[-1].lateStart = self.events[-1].earlyStart
        
        #excluding source and sink nodes
        #their late times are already known
        for i in range(1, len(reversedList)-1):
            n = 0
            #finds the shortest duration dependency
            for activity in reversedList[i-1].dependencies:
                if n == 0:
                    minDuration = activity.duration
                    activity.source.lateStart = activity.target.lateStart - minDuration
                else:
                    if activity.duration < minDuration:
                        minDuration = activity.duration
                        activity.source.lateStart = activity.target.lateStart - minDuration
                n = n+1
            
    def calcFloats(self):
        for activity in activities:
            activities[activity].floatTime = activities[activity].target.lateStart - activities[activity].duration - activities[activity].source.earlyStart
            
    
    def findCriticalActivities(self):
        criticalActivities = []
        for activity in activities:
            if activities[activity].floatTime == 0:
                criticalActivities.append(activity)
                
        self.criticalActivities = criticalActivities
        # these activities are likely out of order and need to be ordered
    
    def criticalPath(self):
        return None
    
    def workerEstimate(self):
        return None
    
    def createSchedule(self):
        return None

activities = {
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
event_1 = Event(1, [ activities['A'] ])
event_2 = Event(2, [ activities['B'], activities['D'] ])
event_3 = Event(3, [ activities['C'] ])

dummy_34 = DummyActivity(event_3)

event_4 = Event(4, [ activities['E'], dummy_34])
event_5 = Event(5, [ activities['F'],  activities['G'] ])
event_6 = Event(6, [ activities['H'] ])

activities['A'].source = event_0
activities['A'].target = event_1

activities['B'].source = event_0
activities['B'].target = event_2

activities['C'].source = event_1
activities['C'].target = event_3

activities['D'].source = event_1
activities['D'].target = event_2

activities['E'].source = event_2
activities['E'].target = event_4

activities['F'].source = event_4
activities['F'].target = event_5

activities['G'].source = event_3
activities['G'].target = event_5

activities['H'].source = event_5
activities['H'].target = event_6

P1 = Project([event_0, event_1, event_2, event_3, event_4, event_5, event_6])
P1.orderEvents()
P1.calcEarlyTimes()
P1.calcLateTimes()
P1.calcFloats()
P1.findCriticalActivities()

for event in P1.events:
    print(event.identifier, event.earlyStart, event.lateStart)


#Problems:
    # in P1.events, events 2 and 3 are the wrong way around
    # all early times are correct, but all late times except 0,5,6 are wrong
