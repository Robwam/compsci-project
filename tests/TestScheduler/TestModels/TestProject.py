import TestScheduler.mock_data as mock_data

from Scheduler.Models.Project import Project
from Scheduler.Models.Activity import Activity, DummyActivity

from nose.tools import assert_equal, assert_raises

import copy

class TestProject():
    def __init__(self):
        self.test_project = None

    # Called automatically by nose
    def setUp(self):
        self.test_project = Project(copy.copy(mock_data.m1_events), copy.copy(mock_data.m1_activities))
        self.test_project_no_source = Project(copy.copy(mock_data.no_source_events), copy.copy(mock_data.no_source_activities))
        self.test_project_unorderable = Project(copy.copy(mock_data.unorderable_events), copy.copy(mock_data.unorderable_activities))

    # Testing algorithm only looks at 1 correct set, however there may be multiple correct sets
    def test_order_events(self):
        self.test_project.order_events()
        assert_equal([o.identifier for o in self.test_project.events], ['source','A','C','B,D','C,E','F,G','sink'])

        # Test validation errors
        assert_raises(Exception, self.test_project_no_source.order_events)
        assert_raises(Exception, self.test_project_unorderable.order_events)

    # Test nothing returned from sink event
    def test_activities_from_event_no_activities_from_sink(self):
        result = self.test_project.activities_from_event(mock_data.m1_event6)
        # Edge case
        assert_equal(result, [])

    # Test activities F and G are returned from m1_event5
    def test_activities_from_event_non_empty_result(self):
        result = self.test_project.activities_from_event(self.test_project.event_by_identitifer('A'))
        # Normal case
        assert_equal(result, [self.test_project.activity_by_name('C'), self.test_project.activity_by_name('D')])

    # Test correct float_times for all activities
    def test_calc_floats(self):
        # Mock events and activities
        event1 = copy.copy(mock_data.m1_event1)
        event1.early_start_time = 4

        event2 = copy.copy(mock_data.m1_event3)
        event2.late_start_time = 7

        self.test_project.activities = [Activity('Activity', 2, event1, event2)]

        self.test_project.calc_floats()

        # Normal case
        assert_equal(self.test_project.activities[0].float_time, 1)

    def test_calc_early_start_time(self):
        self.test_project.calc_early_start_time()

        # Edge case
        assert_equal(self.test_project.event_by_identitifer('source').early_start_time, 0)

        # Nomral case
        assert_equal(self.test_project.event_by_identitifer('B,D').early_start_time, 6)

        # Dummy case
        assert_equal(self.test_project.event_by_identitifer('C,E').early_start_time, 9)

        # Edge case
        assert_equal(self.test_project.event_by_identitifer('sink').early_start_time, 16)

    def test_calc_late_start_time(self):
        self.test_project.calc_late_start_time()

        # Edge case
        assert_equal(self.test_project.event_by_identitifer('source').late_start_time, 0)

        # Nomral case
        assert_equal(self.test_project.event_by_identitifer('B,D').late_start_time, 6)

        # Dummy case
        assert_equal(self.test_project.event_by_identitifer('C').late_start_time, 9)

        # Edge case
        assert_equal(self.test_project.event_by_identitifer('sink').late_start_time, 16)


    def test_calc_min_num_worker(self):
        self.test_project.critical_path_length = 10
        self.test_project.activities = [Activity('Activity', 2, None, None),
                                        Activity('Activity', 5, None, None),
                                        Activity('Activity', 7, None, None)]


        assert_equal(self.test_project.calc_min_num_worker(), 2)

    def test_naive_schedule_single_worker(self):
        activity1 = Activity('Activity 1', 2, None, None)
        activity2 = DummyActivity('Activity 2', None, None)
        activity3 = Activity('Activity 3', 7, None, None)

        expected = {
            0: [activity3, activity1]
        }

        self.test_project.activities = [activity1, activity2, activity3]

        result = self.test_project.naive_schedule(1) # 1 worker

        assert_equal(result, expected)

    def test_naive_schedule_two_workers(self):
        activity1 = Activity('Activity 1', 2, None, None)
        activity2 = DummyActivity('Activity 2', None, None)
        activity3 = Activity('Activity 3', 7, None, None)

        expected = {
            0: [activity3],
            1: [activity1]
        }

        self.test_project.activities = [activity1, activity2, activity3]

        result = self.test_project.naive_schedule(2) # 2 workers

        assert_equal(result, expected)

    def test_integration_create_schedule_two_workers(self):
        expected = {
            0: [
                self.test_project.activity_by_name('A'),
                self.test_project.activity_by_name('C'),
                self.test_project.activity_by_name('G'),
                self.test_project.activity_by_name('F')],
            1: [self.test_project.activity_by_name('B'),
                self.test_project.activity_by_name('D'),
                self.test_project.activity_by_name('E'),
                self.test_project.activity_by_name('H')]
        }

        result = self.test_project.create_schedule(2) # two worekrs
        assert_equal(result, expected)

    def test_integration_create_schedule_surplus_to_requirement(self):
        result = self.test_project.create_schedule(5) # five worekrs
        assert_equal(len(result.keys()), 2)
