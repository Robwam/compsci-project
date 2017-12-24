# Events connect activities, starting at the source node and ending at the sink node
class Event():
    def __init__(self, identifier, dependencies, earlyStart=0, lateStart=0):
        self.identifier = identifier
        self.dependencies = dependencies
        self.earlyStart = earlyStart
        self.lateStart = lateStart

    def __repr__(self):

# Activities are tasks that come from an event and lead to an event
class Activity():
    def __init__(self, name, duration, source=None, target=None, floatTime=0):
        self.name = name
        self.duration = duration
        self.source = source
        self.target = target
        self.floatTime = floatTime

    def __repr__(self):

class Project():
    def __init__(self, events, activities):

    # Return a list of activities in which can be done
    def orderEvents(self):

    def calcEarlyTimes(self):

    def activitiesFromEvent(self, event):

    def calcLateTimes(self):

    def calcFloats(self):

    def findCriticalActivities(self):

    # NOTE: This only finds a single critical path
    # NOTE: This hangs if there is no critical path
    def criticalPath(self):

    def calc_min_num_worker(self):

    def calc_schedule(self):

    def naive_schedule(self, num_workers):

    def createSchedule(self):
