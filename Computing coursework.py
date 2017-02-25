#Project made up of events

class Event():
    def __init__(self, name, duration, dependencies, earlyStart=0, lateStart=0):
        self.name = name
        self.duration = duration
        self.dependencies = dependencies
        self.earlyStart = earlyStart
        self.lateStart = lateStart


class Project():
    def __init__(self, eventList, dependency):
        self.eventList = list(eventList)

    def orderEvents():
        #obtains list of events in order
        None

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
    

rmWall = Event('Remove old wall',20,None)
pWall = Event('Wallpaper wall', 10, rmWall)
P1 = Project([rmWall,pWall])
#/usr/#05robinsonc
