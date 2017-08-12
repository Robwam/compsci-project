import logging
logger = logging.getLogger(__name__)

# Activities are tasks that come from an event and lead to an event
class Activity():
    def __init__(self, name, duration, source=None, target=None, float_time=0):
        self.name = name
        self.duration = duration
        self.source = source
        self.target = target
        self.float_time = float_time

    def __repr__(self):
        if (self.source and self.target):
            return "%s [%i, %s->%s]" % (self.name, self.duration, self.source.identifier, self.target.identifier)
        else:
            return "%s [%i]" % (self.name, self.duration)

# Dummies are activities with 0 duration
class DummyActivity(Activity):
    def __init__(self, name, source, target=None):
        self.name = name
        self.duration = 0
        self.source = source
        self.target = target
