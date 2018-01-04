from Scheduler.Exceptions import ScheduleError
import math

'''
Static class methods
'''
class ScheduleService(object):

    '''
    Returns list of events in dependency ordered

    Args:
        [Event] events - A list of events to order

    Returns:
        [Event] - A list of events
    '''
    def order_events(events):
        ordered = []
        event_list = list(events)

        # Check we have a source event
        source_event = False
        for event in event_list:
            if len(event.dependencies) == 0:
                source_event = True

        if not source_event:
            raise ScheduleError('No source event')

        # Adds events to orrdered list in dependency order
        while len(event_list) > 0:
            event_added = False
            for event in event_list:
                add_event = True
                for dep in sorted(event.dependencies, key=lambda a: a.name):
                    if dep.source not in ordered:
                        add_event = False
                        break

                if add_event:
                    ordered.append(event)
                    event_list.remove(event)
                    event_added = True

            if event_added == False:
                raise ScheduleError('Events unorderable')

        return ordered

    '''
    Updates ordered activities a list of activities in order

    Args:
        [Event] ordered_events - A list of ordered events

    Returns:
        [Activity] - A list of ordered activities
    '''
    def order_activities(ordered_events):
        activities = []
        for event in ordered_events:
            activities += sorted(event.activities_from_event, key=lambda a: a.name) # Add two lists together

        return list(reversed(activities))

    '''
    Updates early starts of every event

    For each event, finds maximum combination of activity duration and activity sources early starts

    Args:
        [Event] ordered_events - A list of ordered events
    '''
    def calc_early_start_time(ordered_events):
        for event in ordered_events:
            max_early_start_time = 0
            for activity in sorted(event.dependencies, key=lambda a: a.name):
                potential_start = activity.duration + activity.source.early_start_time
                if potential_start > max_early_start_time:
                    max_early_start_time = potential_start

            event.early_start_time = int(max_early_start_time)

    '''
    Updates late start times of every event

    Backwards pass for each event, finds minimum combination
    of activity duration and activity target late start

    Args:
        [Event] ordered_events - A list of ordered events
    '''
    def calc_late_start_time(ordered_events):
        # reversed for backwards pass
        reversed_list = list(reversed(list(ordered_events)))

        # Special cases for sink event
        reversed_list[0].late_start_time = reversed_list[0].early_start_time

        for event in reversed_list[1:]:
            min_late_start_time = math.inf
            for activity in sorted(event.activities_from_event, key=lambda a: a.name):
                potential_late_start_time = activity.target.late_start_time - activity.duration
                if potential_late_start_time < min_late_start_time:
                    min_late_start_time = potential_late_start_time

            event.late_start_time = int(min_late_start_time)

    '''
    Calculates and updates float time for every activity

    Args:
        [Activity] activities - A list of activities

    NOTE events should have late_start_time and early_start_time already calculated
    '''
    def calc_floats(activities):
        for activity in activities:
            activity.float_time = int(activity.target.late_start_time - activity.duration - activity.source.early_start_time)

    '''
    Updates critical_activities property with the crtical activities

    Critical activities are activities with a float of 0

    Args:
        [Activity] activities - A list of activities

    Returns:
        Int - The length of the critical path
    '''
    def calc_critical_path_length(activities):
        critical_activities = []
        for activity in activities:
            if activity.float_time == 0:
                critical_activities.append(activity)

        return sum([a.duration for a in critical_activities])

    '''
    Returns the minimum number of workers

    Divides total sum of duration of activities by length of criticle path and rounds up

    Args:
        Int critical_path_length - The length of the critical path
        [Activity] activities - A list of activities

    Returns:
        Int - The minimum number of workers
    '''
    def calc_min_num_worker(critical_path_length, activities):
        total_time = sum([a.duration for a in activities])
        return math.ceil(total_time / critical_path_length)

    '''
    Calculates a naive schedule using bin packing

    Args:
        Int num_workers - The number of workers to use in the schedule
        [Activity] ordered_activities - A list of ordered activities

    Returns:
        Dict - A dictionary keyed on worker id with values being the activities they are assigned
    '''
    def worker_assignments(num_workers, ordered_activities):
        # Filter out activities with no duration (i.e. dummies)
        activities = list(filter(lambda activity: activity.duration != 0, ordered_activities))

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
        [Activity] activities - A list of activities

    Returns:
        Activity - The corresponding activity
    '''
    def activity_by_name(activity_name, activities):
        for activity in activities:
            if activity.name == activity_name:
                return activity

        return None

    '''
    Returns an event corresponding to its identifier

    Args:
        Str identifier - The name of the event
        [Event] events - A list of events

    Returns:
        Event - The corresponding event
    '''
    def event_by_identitifer(identifier, events):
        for event in events:
            if event.identifier == identifier:
                return event

        return None

    '''
    Main schedule function, does scheduling actions in order and returns
    worker schedule assignments

    Args:
        [Event] events - A list of events
        Int workers - The number of workers. If none or if surplus
                      to requirement we use the min based on critical
                      activity length. Defaults to None.

    Returns:
        Dict - The worker schedule assignments
    '''
    def create_schedule(events, num_of_workers=None):
        ordered_events = ScheduleService.order_events(events)
        ordered_activities = ScheduleService.order_activities(ordered_events)

        if (len(ordered_activities) == 0):
            raise ScheduleError('No activities to schedule')

        ScheduleService.calc_early_start_time(ordered_events)
        ScheduleService.calc_late_start_time(ordered_events)
        ScheduleService.calc_floats(ordered_activities)

        critical_path_length = ScheduleService.calc_critical_path_length(ordered_activities)
        min_num_workers = ScheduleService.calc_min_num_worker(critical_path_length, ordered_activities)

        # Set the worker count to the minimum number of workers if
        if not num_of_workers or num_of_workers > min_num_workers:
            num_of_workers = min_num_workers

        return ScheduleService.worker_assignments(num_of_workers, ordered_activities)
