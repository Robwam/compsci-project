import math

import logging
logger = logging.getLogger(__name__)

# Events connect activities, starting at the source node and ending at the sink node
class Event():
    def __init__(self, identifier, dependencies, early_start_time=0, lateStart=0):
        self.identifier = identifier
        self.dependencies = dependencies
        self.early_start_time = early_start_time
        self.lateStart = lateStart

    def __repr__(self):
        if self.early_start_time == math.inf:
            early_start = 'inf'
        else:
            early_start = str(self.early_start_time)

        if self.lateStart == math.inf:
            lateStart = 'inf'
        else:
            lateStart = str(self.lateStart)

        return "%s [%s|%s, [%s]]" % (self.identifier, early_start, lateStart, ','.join([d.name for d in self.dependencies])) # - %i - %s" % (self.name, self.duration, self.dependencies)
