from Scheduler.Models.Event import Event
from Scheduler.Models.Activity import Activity, DummyActivity

# ORDERABLE EVENTS

# https://revisionworld.com/a2-level-level-revision/maths/decision-maths-0/critical-path-analysis
# Event(identifier, dependencies)
m1_event0 = Event('source', [])
m1_event1 = Event('A', [])
m1_event2 = Event('B,D', [])
m1_event3 = Event('C', [])
m1_event4 = Event('C,E', [])
m1_event5 = Event('F,G', [])
m1_event6 = Event('sink', [])

# Activity(name, duration, source, target)
m1_activity_a = Activity('A', 3, m1_event0, m1_event1)
m1_activity_b = Activity('B', 5, m1_event0, m1_event2)
m1_activity_c = Activity('C', 2, m1_event1, m1_event3)
m1_activity_d = Activity('D', 3, m1_event1, m1_event2)
m1_activity_e = Activity('E', 3, m1_event2, m1_event4)
m1_activity_f = Activity('F', 5, m1_event4, m1_event5)
m1_activity_g = Activity('G', 1, m1_event3, m1_event5)
m1_activity_h = Activity('H', 2, m1_event5, m1_event6)

m1_dummy_activity_event_3_4 = DummyActivity('C_dummy', m1_event3, m1_event4)

# Write out dependencies
m1_event1.dependencies = [m1_activity_a]
m1_event2.dependencies = [m1_activity_b, m1_activity_d]
m1_event3.dependencies = [m1_activity_c]
m1_event4.dependencies = [m1_activity_e, m1_dummy_activity_event_3_4]
m1_event5.dependencies = [m1_activity_f, m1_activity_g]
m1_event6.dependencies = [m1_activity_h]

m1_events = [m1_event0, m1_event1, m1_event2, m1_event3, m1_event4, m1_event5, m1_event6]
m1_activities = [m1_activity_a, m1_activity_b, m1_activity_c, m1_activity_d, m1_activity_e, m1_activity_f, m1_activity_g, m1_activity_h, m1_dummy_activity_event_3_4]

# No source events
# Due to a loop

no_source_event0 = Event('C',[])
no_source_event1 = Event('A', [])
no_source_event2 = Event('B', [])

#Activity
no_source_activity_a = Activity('A', 1, no_source_event0, no_source_event1)
no_source_activity_b = Activity('B', 2, no_source_event1, no_source_event2)
no_source_activity_c = Activity('C', 4, no_source_event2, no_source_event0)

#Dependencies
no_source_event0.dependencies = [no_source_activity_c]
no_source_event1.dependencies = [no_source_activity_a]
no_source_event2.dependencies = [no_source_activity_b]

no_source_events = [no_source_event0,no_source_event1,no_source_event2]
no_source_activities = [no_source_activity_a, no_source_activity_b, no_source_activity_c]

# Unorderable events
unorderable_event0 = Event('source',[])
unorderable_event1 = Event('A,D',[])
unorderable_event2 = Event('B',[])
unorderable_event3 = Event('C',[])

# Unorderable activities
unorderable_activity_a = Activity('A', 1, unorderable_event0, unorderable_event1)
unorderable_activity_b = Activity('B', 2, unorderable_event1, unorderable_event2)
unorderable_activity_c = Activity('C', 7, unorderable_event2, unorderable_event3)
unorderable_activity_d = Activity('D', 4, unorderable_event3, unorderable_event1)

unorderable_event1.dependencies = [unorderable_activity_a]
unorderable_event2.dependencies = [unorderable_activity_b, unorderable_activity_d]
unorderable_event3.dependencies = [unorderable_activity_c]

unorderable_events = [unorderable_event0,unorderable_event1,unorderable_event2,unorderable_event3]
unorderable_activities = [unorderable_activity_a,unorderable_activity_b,unorderable_activity_c,unorderable_activity_d]
