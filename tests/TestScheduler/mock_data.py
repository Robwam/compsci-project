from Scheduler.Models.Event import Event
from Scheduler.Models.Activity import Activity

# ORDERABLE EVENTS

# https://revisionworld.com/a2-level-level-revision/maths/decision-maths-0/critical-path-analysis
# Event(identifier, dependencies)
m1_event_source = Event(identifier='source', [])
m1_event_A = Event(identifier='A', [])
m1_event_BD = Event(identifier='B,D', [])
m1_event_C = Event(identifier='C', [])
m1_event_CE = Event(identifier='C,E', [])
m1_event_FG = Event(identifier='F,G', [])
m1_event_sink = Event(identifier='sink', [])

# Activity(name, duration, source, target)
m1_activity_a = Activity('A', 3, m1_event_source, m1_event_A)
m1_activity_b = Activity('B', 5, m1_event_source, m1_event_BD)
m1_activity_c = Activity('C', 2, m1_event_A, m1_event_C)
m1_activity_d = Activity('D', 3, m1_event_A, m1_event_BD)
m1_activity_e = Activity('E', 3, m1_event_BD, m1_event_CE)
m1_activity_f = Activity('F', 5, m1_event_CE, m1_event_FG)
m1_activity_g = Activity('G', 1, m1_event_C, m1_event_FG)
m1_activity_h = Activity('H', 2, m1_event_FG, m1_event_sink)

m1_dummy_activity_event_3_4 = Activity('C_dummy', 0, m1_event_C, m1_event_CE)

# Write out dependencies
m1_event_A.dependencies = [m1_activity_a]
m1_event_BD.dependencies = [m1_activity_b, m1_activity_d]
m1_event_C.dependencies = [m1_activity_c]
m1_event_CE.dependencies = [m1_activity_e, m1_dummy_activity_event_3_4]
m1_event_FG.dependencies = [m1_activity_f, m1_activity_g]
m1_event_sink.dependencies = [m1_activity_h]

m1_events = [m1_event_source, m1_event_A, m1_event_BD, m1_event_C, m1_event_CE, m1_event_FG, m1_event_sink]
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
