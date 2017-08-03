import math

import logging
logger = logging.getLogger('root')

# The overarching project that needs to be completed
# Made up of events happening in sequence

class Project():
    def __init__(self, events, activities):
        self.events = events
        self.activities = activities


    def order_events(self):
        ordered = []
        eventList = self.events

        # Check we have a source event
        source_event = False
        for event in eventList:
            if event.dependencies == []:
                source_event = True

        if not source_event:
            raise Exception('No source event')


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
                raise Exception('Events unorderable')

        self.events = ordered

    def order_activites(self):
        self.order_events()

        activities = []
        for event in self.events:
            activities += self.activitiesFromEvent(event) # Add two lists together

        return reversed(activities)

    def calcEarlyTimes(self):
        for event in self.events:
            maxEarlyStart = 0
            for activity in event.dependencies:
                potentialStart = activity.duration + activity.source.earlyStart
                if potentialStart > maxEarlyStart:
                    maxEarlyStart = potentialStart

            event.earlyStart = maxEarlyStart

    def activitiesFromEvent(self, event):
        out_activities = []
        for activity in self.activities:
            if activity.source == event:
                out_activities.append(activity)

        return out_activities

    def calcLateTimes(self):
        # reversed for backwards pass
        reversedList = list(reversed(self.events))

        #special cases for sink event
        self.events[-1].lateStart = self.events[-1].earlyStart

        for event in reversedList[1:]:
            min_lateStart = math.inf
            for activity in self.activitiesFromEvent(event):
                potentialLateTime = activity.target.lateStart - activity.duration
                if potentialLateTime < min_lateStart:
                    min_lateStart = potentialLateTime

            event.lateStart = min_lateStart

    def calcFloats(self):
        for activity in self.activities:
            activity.floatTime = activity.target.lateStart - activity.duration - activity.source.earlyStart

    def findCriticalActivities(self):
        criticalActivities = []
        for activity in self.activities:
            if activity.floatTime == 0:
                criticalActivities.append(activity)

        self.criticalActivities = criticalActivities
        # these activities are likely out of order and need to be ordered

    # NOTE: This only finds a single criticle path
    # NOTE: This hangs if there is no criticle path
    def criticalPath(self):
        events_path = []
        activities_path = []
        nextEvent = self.events[0]
        events_path.append(nextEvent)
        last = False
        while (not last):


            # Check if this is the sink event, if so break
            if nextEvent == self.events[-1]:
                last = True

            # Look at all out activities, choose a criticle one
            for activity in self.activitiesFromEvent(nextEvent):
                if activity in self.criticalActivities:
                    activities_path.append(activity)
                    nextEvent = activity.target
                    break

            events_path.append(nextEvent)

        for activity in self.activitiesFromEvent(nextEvent):
            if activity in self.criticalActivities:
                activities_path.append(activity)

        self.critcle_activities_path = activities_path
        self.critcle_events_path = events_path
        self.criticle_path_length = sum([a.duration for a in self.critcle_activities_path])

    def calc_min_num_worker(self):
        total_time = sum([a.duration for a in self.activities])
        return math.ceil(total_time / self.criticle_path_length)

    def calc_schedule(self):
        pass

    def naive_schedule(self, num_workers):
        # NOTE these should already be in order!
        jobs = self.order_activites()

        jobs = list(filter(lambda j: j.duration != 0, jobs))

        workers_jobs = {}

        for worker in range(0, num_workers):
            workers_jobs[worker] = []

        while len(jobs) > 0:
            for worker in workers_jobs:
                if len(jobs) > 0:
                    workers_jobs[worker].append(jobs.pop())
                else:
                    break

        return workers_jobs

    def createSchedule(self, workers=None):
        self.order_events()
        self.calcEarlyTimes()
        self.calcLateTimes()
        self.calcFloats()
        self.findCriticalActivities()
        self.criticalPath()

        min_num_workers = self.calc_min_num_worker()

        # Set the worker count to the miniumum number of workers if
        if not workers or workers > min_num_workers:
            workers = min_num_workers

        return self.naive_schedule(workers)
