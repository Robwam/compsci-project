import math

# The overarching project that needs to be completed
# Made up of events happening in sequence

'''
Given events and activities can produce worker assignments
'''
class Project():

    '''
    Initilise the project

    Args:
        [Event] events - The scheduling project events
        [Activity] activities - The scheduling project activities
    '''
    def __init__(self, events, activities):
        self.events = events
        self.activities = activities

    '''
    Updates events property to be ordered
    '''
    def order_events(self):
        ordered = []
        event_list = self.events

        # Check we have a source event
        source_event = False
        for event in event_list:
            if event.dependencies == []:
                source_event = True

        if not source_event:
            raise Exception('No source event')


        # Adds events to ordered list in dependency order
        while len(event_list) > 0:
            event_added = False
            for event in event_list:
                add_event = True
                for dep in event.dependencies:
                    if dep.source not in ordered:
                        add_event = False
                        break

                if add_event:
                    ordered.append(event)
                    event_list.remove(event)
                    event_added = True

            if event_added == False:
                raise Exception('Events unorderable')

        self.events = ordered

    '''
    Updates ordered activities a list of activities in order

    NOTE: Assumes events are in order
    '''
    def order_activities(self):
        activities = []
        for event in self.events:
            activities += self.activities_from_event(event) # Add two lists together

        self.activities = list(reversed(activities))

    '''
    Updates early starts of every event

    For each event, finds maximum combination of activity duration and activity sources early starts
    '''
    def calc_early_start_time(self):
        for event in self.events:
            max_early_start_time = 0
            for activity in event.dependencies:
                potential_start = activity.duration + activity.source.early_start_time
                if potential_start > max_early_start_time:
                    max_early_start_time = potential_start

            event.early_start_time = max_early_start_time

    '''
    Returns a list of activities whose source is the event

    Args:
        Event event - The event

    Returns:
        [Activity] - The activities from this event
    '''
    def activities_from_event(self, event):
        out_activities = []
        for activity in self.activities:
            if activity.source == event:
                out_activities.append(activity)

        return out_activities

    '''
    Updates late start times of every event

    Backwards pass for each event, finds minimum combination
    of activity duration and activity target late start
    '''
    def calc_late_start_time(self):
        # reversed for backwards pass
        reversed_list = list(reversed(self.events))

        # Special cases for sink event
        self.events[-1].late_start_time = self.events[-1].early_start_time

        for event in reversed_list[1:]:
            min_late_start_time = math.inf
            for activity in self.activities_from_event(event):
                potential_late_start_time = activity.target.late_start_time - activity.duration
                if potential_late_start_time < min_late_start_time:
                    min_late_start_time = potential_late_start_time

            event.late_start_time = min_late_start_time

    '''
    Calculates and updates float time for every activity

    NOTE events should have late_start_time and early_start_time already calculated
    '''
    def calc_floats(self):
        for activity in self.activities:
            activity.float_time = activity.target.late_start_time - activity.duration - activity.source.early_start_time

    '''
    Updates critical_activities property with the crtical activities

    Critical activities are activities with a float of 0

    TODO these activities are likely out of order and need to be ordered

    NOTE this function is trivial in complexity therefore does not require testing
    '''
    def find_critical_activities(self):
        critical_activities = []
        for activity in self.activities:
            if activity.float_time == 0:
                critical_activities.append(activity)

        self.critical_activities = critical_activities
        self.critical_path_length = sum([a.duration for a in critical_activities])

    '''
    Returns the minimum number of workers

    Devides total sum of duration of activities by length of criticle path and rounds up

    Returns:
        Int - The minimum number of workers
    '''
    def calc_min_num_worker(self):
        total_time = sum([a.duration for a in self.activities])
        return math.ceil(total_time / self.critical_path_length)

    '''
    Calculates a naive schedule using bin packing

    Args:
        Int num_workers - The number of workers to use in the schedule

    Returns:
        Dict - A dictionary keyed on worker id with values being the activities they are assigned
    '''
    def naive_schedule(self, num_workers):
        # Filter out activities with no duration (i.e. dummies)
        activities = list(filter(lambda activity: activity.duration != 0, self.activities))

        worker_activities = {}

        for worker in range(0, num_workers):
            worker_activities[worker] = []

        while len(activities) > 0:
            for worker_id in worker_activities:
                if len(activities) > 0:
                    worker_activities[worker_id].append(activities.pop())
                else:
                    break

        return worker_activities

    '''
    Returns an activity corresponding to its name

    Args:
        Str activity_name - The name of the activity

    Returns:
        Activity - The corresponding activity
    '''
    def activity_by_name(self, activity_name):
        for activity in self.activities:
            if activity.name == activity_name:
                return activity

        return None

    '''
    Returns an event corresponding to its identifier

    Args:
        Str identifier - The name of the event

    Returns:
        Event - The corresponding event
    '''
    def event_by_identitifer(self, identifier):
        for event in self.events:
            if event.identifier == identifier:
                return event

        return None

    '''
    Main schedule function, does scheduling actions in order and returns
    worker schedule assignments

    Args:
        Int workers - The number of workers. If none or if surplus
                      to requirement we use the min based on critical
                      activty length.

    Returns:
        Dict - The worker schedule assignments
    '''
    def create_schedule(self, workers=None):
        self.order_events()
        self.calc_early_start_time()
        self.calc_late_start_time()
        self.calc_floats()
        self.find_critical_activities()
        self.order_activities()

        min_num_workers = self.calc_min_num_worker()

        # Set the worker count to the minimum number of workers if
        if not workers or workers > min_num_workers:
            workers = min_num_workers

        return self.naive_schedule(workers)
