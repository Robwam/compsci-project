from Scheduler.Configuration.database import DB
from pony.orm import *

'''
Given events and activities can produce worker assignments
'''
class Project(DB.Entity):
    name = Optional(str)
    number_of_workers = Optional(int)
    activities = Set('Activity')
    events = Set('Event')
