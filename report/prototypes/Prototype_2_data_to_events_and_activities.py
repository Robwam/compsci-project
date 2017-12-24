def data_to_events_and_activities(data):
    # Convert csv dependencies into list
    # NOTE we sort dependencies so they are order indepenent
    for row in data:
        if row[2] == '': # If no dependencies, add empty list
            row.append([])
        else:
            row.append(sorted(row[2].split(',')))
            row[2] = ','.join(row[3])

    # Create Events
    unique_dependencies = {}
    for row in data:
        if row[2] not in unique_dependencies and row[3] != []:
            unique_dependencies[row[2]] = row[3]

    events = {
        'source': Event('source', []),
        'sink': Event('sink', [])
    }

    for dependencies in unique_dependencies:
        events[dependencies] = Event(dependencies, [])

    # Create activities and update their source events
    activities = {}
    for row in data:
        if row[3] == []:
            source = events['source']
        else:
            source = events[row[2]]

        activities[row[0]] = Activity(row[0], row[1], source, None)

    dummies = {}

    # Update the activities target events
    for activity_key, activity in activities.items():
        potential_targets = list(filter(lambda s: activity_key in s, unique_dependencies))
        if len(potential_targets) == 0:
            activity.target = events['sink']
            events['sink'].dependencies.append(activity)
        elif len(potential_targets) == 1:
            activity.target = events[potential_targets[0]]
        elif len(potential_targets) == 2: # TODO More cases
            if (potential_targets[0] == activity_key):
                i, j = [0, 1]
            elif (potential_targets[1] == activity_key):
                i, j = [1, 0]
            else:
                print('We need a dummy! Not covered', activity_key, potential_targets)
                continue

            activity.target = events[potential_targets[i]]
            dummies[activity_key + '_dummy'] = DummyActivity(activity_key + '_dummy', events[potential_targets[i]], events[potential_targets[j]])
            e = events[potential_targets[j]]
            e.dependencies.append(dummies[activity_key + '_dummy'])
        else:
            print('We need a dummy!', activity_key, potential_targets)

    # Merge dummies with real
    activities = {**activities, **dummies}

    # Link events & activities
    for event in events.values():

        for dep in event.identifier.split(','):
            if dep in ['source', 'sink']: # TODO check dis
                continue
            if dep + '_dummy' in [s.name for s in event.dependencies]:
                continue
            event.dependencies.append(activities[dep])

    return [list(events.values()), list(activities.values())]
