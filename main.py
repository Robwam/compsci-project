#!/usr/bin/env python3

# this is my computing project prototype

class Project():
    def __init__(self, events, startTime=0):
        self.events = events
        self.starTime = startTime

    def eventOrder(self):
        ordered = []
        events = list(self.events)

        # TODO infinite loop if dependencies wrong
        while len(events) > 0:
            for event in events:
                shouldAdd = True
                for dep in event.dependencies:
                    if dep not in ordered:
                        shouldAdd = False
                        break
                if shouldAdd:
                    ordered.append(event)
                    events.remove(event)
        return ordered

class Event():
    def __init__(self, name, duration, dependencies):
        self.name = name
        self.duration = duration
        self.dependencies = dependencies

    def __repr__(self):
        return "%s" % self.name# - %i - %s" % (self.name, self.duration, self.dependencies)

e1 = Event('test1', 2, [])
e3 = Event('test3',4,[e1])
e2 = Event('test2', 3, [e1,e3])

p1 = Project([e1,e2,e3])
print(p1.eventOrder())
