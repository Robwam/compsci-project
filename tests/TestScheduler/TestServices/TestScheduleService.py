from Scheduler.Configuration import database
from Scheduler.Services.ScheduleService import ScheduleService
from Scheduler.Models.Project import Project
from Scheduler.Models.Event import Event
from Scheduler.Models.Activity import Activity
from Scheduler.Exceptions import ScheduleError

from unittest import TestCase
from nose.tools import assert_equal, assert_raises, nottest

import pony.orm

class TestScheduleService(TestCase):

    test_database_filename = "projects.test.db"

    def setup_class():
        database.setup(TestScheduleService.test_database_filename)

    def teardown_class():
        database.teardown(TestScheduleService.test_database_filename)

    def tearDown(self):
        database.DB.drop_all_tables(True)

    def setUp(self):
        database.DB.create_tables()
        with pony.orm.db_session:
            self.setup_mock_data()

    # Testing algorithm only looks at 1 correct set, however there may be multiple correct sets
    @pony.orm.db_session
    def test_order_events(self):
        events = Project.get(name="mock").events
        no_source_events = Project.get(name="no_source_events").events
        unorderable_events = Project.get(name="unorderable_events").events

        # NOTE there are two correct orderings, test both
        expected_1 = ['source','A','C','B,D','C,E','F,G','sink']
        expected_2 = ['source','A','B,D','C','C,E','F,G','sink']

        actual = [o.identifier for o in ScheduleService.order_events(events)]
        assert(actual == expected_1 or actual == expected_2)

        # Test validation errors
        assert_raises(ScheduleError, ScheduleService.order_events, no_source_events)
        assert_raises(ScheduleError, ScheduleService.order_events, unorderable_events)

    # Test correct float_times for all activities
    @pony.orm.db_session
    def test_calc_floats(self):
        # Mock events and activities
        event1 = Event.get(identifier='A')
        event1.early_start_time = 4

        event2 = Event.get(identifier='C')
        event2.late_start_time = 7

        activities = [Activity(name='Activity', duration=2, source=event1, target=event2)]

        actual = ScheduleService.calc_floats(activities)

        # Normal case
        assert_equal(activities[0].float_time, 1)

    @pony.orm.db_session
    def test_calc_early_start_time(self):
        events = ScheduleService.order_events(Project.get(name="mock").events)
        ScheduleService.calc_early_start_time(events)

        # Edge case
        assert_equal(Event.get(identifier='source').early_start_time, 0)

        # Nomral case
        assert_equal(Event.get(identifier='B,D').early_start_time, 6)

        # Dummy case
        assert_equal(Event.get(identifier='C,E').early_start_time, 9)

        # Edge case
        assert_equal(Event.get(identifier='sink').early_start_time, 16)

    @pony.orm.db_session
    def test_calc_late_start_time(self):
        events = ScheduleService.order_events(Project.get(name="mock").events)
        ScheduleService.calc_early_start_time(events)
        ScheduleService.calc_late_start_time(events)

        # Edge case
        assert_equal(Event.get(identifier='source').late_start_time, 0)

        # Nomral case
        assert_equal(Event.get(identifier='B,D').late_start_time, 6)

        # Dummy case
        assert_equal(Event.get(identifier='C').late_start_time, 9)

        # Edge case
        assert_equal(Event.get(identifier='sink').late_start_time, 16)

    @pony.orm.db_session
    def test_calc_min_num_worker(self):
        activities = [
            Activity(name='Activity', duration=2, source=None, target=None),
            Activity(name='Activity', duration=5, source=None, target=None),
            Activity(name='Activity', duration=7, source=None, target=None)
        ]

        actual = ScheduleService.calc_min_num_worker(critical_path_length=10, activities=activities)

        assert_equal(actual, 2)

    @pony.orm.db_session
    def worker_assignments_single_worker(self):
        activity1 = Activity(name='Activity 1', duration=2, source=None, target=None)
        activity2 = Activity(name='Activity 2 dummy', duration=0, source=None, target=None)
        activity3 = Activity(name='Activity 3', duration=7, source=None, target=None)

        activities = [activity1, activity2, activity3]

        actual = ScheduleService.worker_assignments(num_workers=1, ordered_activities=activities)

        expected = {
            0: [activity3, activity1]
        }

        assert_equal(actual, expected)

    @pony.orm.db_session
    def worker_assignments_two_workers(self):
        activity1 = Activity(name='Activity 1', duration=2, source=None, target=None)
        activity2 = Activity(name='Activity 2 dummy', duration=0, source=None, target=None)
        activity3 = Activity(name='Activity 3', duration=7, source=None, target=None)

        activities = [activity1, activity2, activity3]

        actual = ScheduleService.worker_assignments(num_workers=2, ordered_activities=activities)

        expected = {
            0: [activity3],
            1: [activity1]
        }

        assert_equal(actual, expected)

    @pony.orm.db_session
    def test_integration_create_schedule_two_workers(self):
        events = Project.get(name="mock").events
        events = ScheduleService.order_events(events)
        activities = ScheduleService.order_activities(events)

        expected = {
            0: [
                ScheduleService.activity_by_name('A', activities),
                ScheduleService.activity_by_name('C', activities),
                ScheduleService.activity_by_name('G', activities),
                ScheduleService.activity_by_name('F', activities)
            ],
            1: [
                ScheduleService.activity_by_name('B', activities),
                ScheduleService.activity_by_name('D', activities),
                ScheduleService.activity_by_name('E', activities),
                ScheduleService.activity_by_name('H', activities)
            ]
        }

        actual = ScheduleService.worker_assignments(num_workers=2, ordered_activities=activities)
        assert_equal(actual, expected)

    @pony.orm.db_session
    def test_integration_create_schedule_surplus_to_requirement(self):
        events = Project.get(name="mock").events
        actual = ScheduleService.create_schedule(events=events, num_of_workers=5) # five worekrs
        assert_equal(len(actual.keys()), 2)

    def setup_mock_data(self):
        # ORDERABLE EVENTS
        mock_project = Project(name="mock")

        # https://revisionworld.com/a2-level-level-revision/maths/decision-maths-0/critical-path-analysis
        # Event(identifier, dependencies)
        m1_event_source = Event(identifier='source', project=mock_project)
        m1_event_A = Event(identifier='A', project=mock_project)
        m1_event_BD = Event(identifier='B,D', project=mock_project)
        m1_event_C = Event(identifier='C', project=mock_project)
        m1_event_CE = Event(identifier='C,E', project=mock_project)
        m1_event_FG = Event(identifier='F,G', project=mock_project)
        m1_event_sink = Event(identifier='sink', project=mock_project)

        # Activity(name, duration, source, target)
        m1_activity_a = Activity(name='A', duration=3, source=m1_event_source, target=m1_event_A, project=mock_project)
        m1_activity_b = Activity(name='B', duration=5, source=m1_event_source, target=m1_event_BD, project=mock_project)
        m1_activity_c = Activity(name='C', duration=2, source=m1_event_A, target=m1_event_C, project=mock_project)
        m1_activity_d = Activity(name='D', duration=3, source=m1_event_A, target=m1_event_BD, project=mock_project)
        m1_activity_e = Activity(name='E', duration=3, source=m1_event_BD, target=m1_event_CE, project=mock_project)
        m1_activity_f = Activity(name='F', duration=5, source=m1_event_CE, target=m1_event_FG, project=mock_project)
        m1_activity_g = Activity(name='G', duration=1, source=m1_event_C, target=m1_event_FG, project=mock_project)
        m1_activity_h = Activity(name='H', duration=2, source=m1_event_FG, target=m1_event_sink, project=mock_project)

        m1_dummy_activity_event_3_4 = Activity(name='C_dummy', duration=0, source=m1_event_C, target=m1_event_CE, project=mock_project)



        no_source_events_project = Project(name="no_source_events")

        # No source events
        # Due to a loop
        no_source_event0 = Event(identifier='NS_C', project=no_source_events_project)
        no_source_event1 = Event(identifier='NS_A', project=no_source_events_project)
        no_source_event2 = Event(identifier='NS_B', project=no_source_events_project)

        #Activity
        no_source_activity_a = Activity(name='NS_A', duration=1, source=no_source_event0, target=no_source_event1, project=no_source_events_project)
        no_source_activity_b = Activity(name='NS_B', duration=2, source=no_source_event1, target=no_source_event2, project=no_source_events_project)
        no_source_activity_c = Activity(name='NS_C', duration=4, source=no_source_event2, target=no_source_event0, project=no_source_events_project)

        unorderable_events_project = Project(name="unorderable_events")

        # Unorderable events
        unorderable_event0 = Event(identifier='UA_source', project=unorderable_events_project)
        unorderable_event1 = Event(identifier='UA_A,D', project=unorderable_events_project)
        unorderable_event2 = Event(identifier='UA_B', project=unorderable_events_project)
        unorderable_event3 = Event(identifier='UA_C', project=unorderable_events_project)

        # Unorderable activities
        unorderable_activity_a = Activity(name='UA_A', duration=1, source=unorderable_event0, target=unorderable_event1, project=unorderable_events_project)
        unorderable_activity_b = Activity(name='UA_B', duration=2, source=unorderable_event1, target=unorderable_event2, project=unorderable_events_project)
        unorderable_activity_c = Activity(name='UA_C', duration=7, source=unorderable_event2, target=unorderable_event3, project=unorderable_events_project)
        unorderable_activity_d = Activity(name='UA_D', duration=4, source=unorderable_event3, target=unorderable_event1, project=unorderable_events_project)
