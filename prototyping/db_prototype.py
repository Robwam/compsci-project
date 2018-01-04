#!/usr/bin/env python3

from pony.orm import *

db = Database()

class Project(db.Entity):
    name = Required(str)
    number_of_workers = Required(int)
    activities = Set('Activity')
    events = Set('Event')

class Event(db.Entity):
    identifier = Required(str)
    early_start_time = Required(int)
    late_start_time = Required(int)
    project = Required('Project')

    dependencies = Set('Activity')
    activities_from_event = Set('Activity')

class Activity(db.Entity):
    name = Required(str)
    duraiton = Required(int)
    float_time = Required(int)
    source_event = Required('Event', reverse='activities_from_event')
    target_event = Required('Event', reverse='dependencies')
    project = Required('Project')

db.bind(provider='sqlite', filename='projects.db')

db.generate_mapping(create_tables=True)
#sql_debug(True)

@db_session
def create_project():
    project = Project(name='Test project', number_of_workers=2)

    event1 = Event(identifier='1', early_start_time=2, late_start_time=3, project=project)
    event2 = Event(identifier='2', early_start_time=4, late_start_time=7, project=project)
    event3 = Event(identifier='3', early_start_time=5, late_start_time=9, project=project)
    event4 = Event(identifier='4', early_start_time=8, late_start_time=12, project=project)

    act1 = Activity(name='1', duraiton=3, float_time=0, source_event=event1, target_event=event2, project=project)
    act2 = Activity(name='2', duraiton=5, float_time=2, source_event=event2, target_event=event3, project=project)
    act3 = Activity(name='3', duraiton=4, float_time=8, source_event=event2, target_event=event4, project=project)
    act4 = Activity(name='4', duraiton=8, float_time=8, source_event=event1, target_event=event4, project=project)

@db_session
def query_project():
    a = Activity.get(name='4')
    e = a.source_event

#create_project()
query_project()
