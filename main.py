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

    def __str__(self):
        return "%s - %i - %s" % (self.name, self.duration, self.dependencies)

e = Event('test', 2, [])
print(e)
