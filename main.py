#!/usr/bin/env python3

# this is my computing project prototype

class Project():
    def __init__(self, events, startTime=0):
        self.events = events
        self.starTime = startTime


class Event():
    def __init__(self, name, duration, dependencies):
        self.name = name
        self.duration = duration
        self.dependencies = dependencies

    def __repr__(self):
        return "%s - %i - %s" % (self.name, self.duration, self.dependencies)

e1 = Event('test1', 2, [])
e2 = Event('test2', 3, [e1])
print(e1)
print(e2)
