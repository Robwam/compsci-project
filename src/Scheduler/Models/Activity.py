from Scheduler.Configuration.database import DB
from pony.orm import *

'''
Activities are tasks that come from an event and lead to an event
'''
class Activity(DB.Entity):
    name = Required(str)
    duration = Required(int, default=0) # NOTE In hours
    float_time = Required(int, default=0)
    source = Optional('Event', reverse='activities_from_event')
    target = Optional('Event', reverse='dependencies')
    project = Optional('Project')

    def __repr__(self):
        if (self.source and self.target):
            return "%s [%i, %s->%s]" % (self.name, self.duration, self.source.identifier, self.target.identifier)
        else:
            return "%s [%i]" % (self.name, self.duration)
