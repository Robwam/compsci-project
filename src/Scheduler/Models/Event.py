from Scheduler.Configuration.database import DB
from pony.orm import *

import math

'''
Events connect activities, starting at the source node and ending at the sink node
'''
class Event(DB.Entity):
    identifier = Required(str)
    early_start_time = Required(int, default=0)
    late_start_time = Required(int, default=0)
    project = Optional('Project')

    dependencies = Set('Activity', cascade_delete=True)
    activities_from_event = Set('Activity', cascade_delete=True)

    def __repr__(self):
        if self.early_start_time == math.inf:
            early_start = 'inf'
        else:
            early_start = str(self.early_start_time)

        if self.late_start_time == math.inf:
            late_start_time = 'inf'
        else:
            late_start_time = str(self.late_start_time)

        return "%s [%s|%s, [%s]]" % (self.identifier, early_start, late_start_time, ','.join([d.name for d in self.dependencies])) # - %i - %s" % (self.name, self.duration, self.dependencies)
