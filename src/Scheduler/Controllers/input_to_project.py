from Scheduler.Models.Activity import Activity
from Scheduler.Models.Event import Event

'''
Takes activity and event data, adds hidden nodes (source/sink/dummies), writes to database

Args:
    Dict data: The filename of the database, defaults to the one set in config
    Project project: The project object to add activities and events
'''
def data_to_events_and_activities(data, project):
    # NOTE we sort dependencies so they are order indepenent
    for row in data:
        if row[2] == '': # If no dependencies, add empty list
            row.append([])
        else:
            row.append(sorted(row[2]))
            row[2] = ','.join(row[3])

    # Create source and sink events
    events = {
        'source': Event(identifier='source', project=project),
        'sink': Event(identifier='sink', project=project)
    }

    # Create events
    unique_dependencies = {}
    for row in data:
        if row[2] not in unique_dependencies and row[3] != []:
            unique_dependencies[row[2]] = row[3]

    for dependencies in unique_dependencies:
        events[dependencies] = Event(identifier=dependencies, project=project)

    # Create activities and update their source events
    activities = {}
    for row in data:
        if row[3] == []:
            source = events['source']
        else:
            source = events[row[2]]

        activities[row[0]] = Activity(name=row[0], duration=row[1], source=source, project=project)

    dummies = {}

    # Update the activities target events
    for activity_key, activity in activities.items():
        potential_targets = list(filter(lambda s: activity_key in s, unique_dependencies))
        if len(potential_targets) == 0:
            activity.target = events['sink']
        elif len(potential_targets) == 1:
            activity.target = events[potential_targets[0]]
        elif len(potential_targets) == 2:
            if (potential_targets[0] == activity_key):
                i, j = [0, 1]
            elif (potential_targets[1] == activity_key):
                i, j = [1, 0]

            activity.target = events[potential_targets[i]]

            # Create a dummy activity
            dummies[activity_key + '_dummy'] = Activity(name=activity_key + '_dummy', source=events[potential_targets[i]], target=events[potential_targets[j]], project=project)
