from main import *

# Event(identifier, dependencies)
event0 = Event('source', [])
event1 = Event('A', [])
event2 = Event('B,D', [])
event3 = Event('C', [])
event4 = Event('C,E', [])
event5 = Event('F,G', [])
event6 = Event('sink', [])

# Activity(name, duration, source, target)
activity_a = Activity('A', 3, event0, event1)
activity_b = Activity('B', 5, event0, event2)
activity_c = Activity('C', 2, event1, event3)
activity_d = Activity('D', 3, event1, event2)
activity_e = Activity('E', 3, event2, event4)
activity_f = Activity('F', 5, event4, event5)
activity_g = Activity('G', 1, event3, event5)
activity_h = Activity('H', 2, event5, event6)

dummy_activity_event_3_4 = DummyActivity('Dummy', event3, event4)

# Write out dependencies
event1.dependencies = [activity_a]
event2.dependencies = [activity_b, activity_d]
event3.dependencies = [activity_c]
event4.dependencies = [activity_e, dummy_activity_event_3_4]
event5.dependencies = [activity_f, activity_g]
event6.dependencies = [activity_h]

events = [event0, event1, event2, event3, event4, event5, event6]
activities = [activity_a, activity_b, activity_c, activity_d, activity_e, activity_f, activity_g, activity_h, dummy_activity_event_3_4]

project = Project(events, activities)
print(project.createSchedule())
