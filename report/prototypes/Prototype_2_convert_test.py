from main import *

data = [
  ['A', 3, ''],
  ['B', 5, ''],
  ['C', 2, 'A'],
  ['D', 3, 'A'],
  ['E', 3, 'B,D'],
  ['F', 5, 'C,E'],
  ['G', 1, 'C'],
  ['H', 2, 'F,G'],
]

events, activities = data_to_events_and_activities(data)

project = Project(events, activities)
print(project.createSchedule())
