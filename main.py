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
    
