from Scheduler.Configuration.database import DB
from pony.orm import *

# Activities are tasks that come from an event and lead to an event
class Activity(DB.Entity):
    name = Required(str)
    duration = Required(int, default=0) # NOTE In hours
    float_time = Required(int, default=0)
    source = Optional('Event', reverse='activities_from_event')
    target = Optional('Event', reverse='dependencies')
    project = Required('Project')

    # def __init__(self, name, duration, source=None, target=None, float_time=0):
    #     self.name = name
    #     self.duration = duration
    #     self.source = source
    #     self.target = target
    #     self.float_time = float_time

    def __repr__(self):
        if (self.source and self.target):
            return "%s [%i, %s->%s]" % (self.name, self.duration, self.source.identifier, self.target.identifier)
        else:
            return "%s [%i]" % (self.name, self.duration)

# # Dummies are activities with 0 duration
# class DummyActivity(Activity):
#     duration = 0
#     source = Required('Event', reverse='activities_from_event')
#
#     # def __init__(self, name, source, target=None):
#     #     self.name = name
#     #     self.duration = 0
#     #     self.source = source
#     #     self.target = target
