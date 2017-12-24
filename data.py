from main import *

activities = {
    'A': Activity('A', 3),
    'B': Activity('B', 5),
    'C': Activity('C', 2),
    'D': Activity('D', 3),
    'E': Activity('E', 3),
    'F': Activity('F', 5),
    'G': Activity('G', 1),
    'H': Activity('H', 2),
}

event_0 = Event(0, [])
event_1 = Event(1, [ activities['A'] ])
event_2 = Event(2, [ activities['B'], activities['D'] ])
event_3 = Event(3, [ activities['C'] ])

dummy_34 = DummyActivity(event_3, source=None)
activities['dummy_34'] = dummy_34

event_4 = Event(4, [ activities['E'], dummy_34])
dummy_34.target = event_4
event_5 = Event(5, [ activities['F'],  activities['G'] ])
event_6 = Event(6, [ activities['H'] ])

activities['A'].source = event_0
activities['A'].target = event_1

activities['B'].source = event_0
activities['B'].target = event_2

activities['C'].source = event_1
activities['C'].target = event_3

activities['D'].source = event_1
activities['D'].target = event_2

activities['E'].source = event_2
activities['E'].target = event_4

activities['F'].source = event_4
activities['F'].target = event_5

activities['G'].source = event_3
activities['G'].target = event_5

activities['H'].source = event_5
activities['H'].target = event_6

P1 = Project([event_0, event_1, event_2, event_3, event_4, event_5, event_6], activities)
#P1.orderEvents()
#P1.calcEarlyTimes()
#P1.calcLateTimes()
#P1.calcFloats()
#P1.findCriticalActivities()

#print(P1.criticalPath())
