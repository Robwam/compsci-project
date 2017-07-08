from main import *

data = [
 ['A', 12, ''],
 ['B', 2, 'A'],
 ['C', 3, 'A'],
 ['D', 5, 'B,C']
]

# Convert csv dependencies into list
# NOTE we sort dependencies so they are order indepenent
for row in data:
    row.append(sorted(row[2].split(',')))
    row[2] = ','.join(row[3])

# Create Events
unique_dependencies = {}
for row in data:
    if row[2] not in unique_dependencies:
        unique_dependencies[row[2]] = row[3]

events = {
    'source': Event('source', []),
    'sink': Event('sink', [])
}

for dependencies in unique_dependencies:
    events[dependencies] = Event(dependencies, [])

# Create Activites and update their source events
activites = {}
for row in data:
    if row[3] == []:
        source = events['source']
    else:
        source = events[row[2]]
    activites[row[0]] = Activity(row[0], row[1], source, None)

# Update the activites target events
for activty_key, activty in activites.items():
    potential_targets = list(filter(lambda s: activty_key in s, unique_dependencies))

    if len(potential_targets) == 1:
        activty.target = events[potential_targets[0]]
    else:
        print('We need a dummy!')
        # TODO

# Point everything without a target at the sink event
for activity in activites.values():
    if activity.target == None:
        activity.target = events['sink']

# Link events & activites
for event in events.values():
    for dep in event.identifier.split(','):
        if dep in ['', 'source', 'sink']: # TODO check dis
            continue
        event.dependencies.append(activites[dep])

print(events.values())
print(activites.values())
