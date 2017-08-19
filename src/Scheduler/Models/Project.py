from Scheduler.Configuration.database import DB
from pony.orm import *
from datetime import datetime

'''
Given events and activities can produce worker assignments
'''
class Project(DB.Entity):
    name = Optional(str)
    number_of_workers = Optional(int)
    has_been_scheduled = Required(bool, default=False)
    created = Required(datetime, default=datetime.now())
    activities = Set('Activity', cascade_delete=True)
    events = Set('Event', cascade_delete=True)
