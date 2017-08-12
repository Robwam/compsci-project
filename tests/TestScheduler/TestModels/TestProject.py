import TestScheduler.mock_data as mock_data

from Scheduler.Models.Project import Project

from nose.tools import assert_equal, assert_raises

class TestProject():
    def __init__(self):
        self.test_project = None

    # Called automatically by nose
    def setUp(self):
        self.test_project = Project(mock_data.m1_events, mock_data.m1_activities)
        self.test_project_no_source = Project(mock_data.no_source_events, mock_data.no_source_activities)
        self.test_project_unorderable = Project(mock_data.unorderable_events, mock_data.unorderable_activities)

    # Testing algorithm only looks at 1 correct set, however there may be multiple correct sets
    def test_order_events(self):
        self.test_project.order_events()
        assert_equal([o.identifier for o in self.test_project.events], ['source','A','C','B,D','C,E','F,G','sink'])

        assert_raises(Exception, self.test_project_no_source.order_events)
        assert_raises(Exception, self.test_project_unorderable.order_events)


    # Test nothing returned from sink event
    def test_activities_from_event_no_activities_from_sink(self):
        result = self.test_project.activities_from_event(mock_data.m1_event6)
        assert_equal(result, [])

    # Test activities F and G are returned from m1_event5
    def test_activities_from_event_non_empty_result(self):
        # As the source event of C and D is m1_event1
        result = self.test_project.activities_from_event(mock_data.m1_event1)
        assert_equal(result, [mock_data.m1_activity_c, mock_data.m1_activity_d])

    # Test correct float_times for all activities
    def test_calc_floats(self):
        # Source/Sink are edge cases, G, D normal cases
        # Correct floats hand calculated
        self.test_project.calc_floats()

        # Source Activity = 0
        assert_equal(self.test_project.activities[0].float_time, 0)

        # Sink Activity = 0
        assert_equal(self.test_project.activities[-1].float_time, 0)

        # Activity G = 8
        assert_equal(self.test_project.activities[6].float_time, 8)

        # Activity D = 0
        assert_equal(self.test_project.activities[3], 0)

    '''
    def test_order_activities(self):
        # self.test_project.order_activities()

    def test_calcEarlyTimes(self):
        self.test_project.calcEarlyTimes()

    def test_calcLateTimes(self):
        self.test_project.calcLateTimes()



    def test_findCriticalActivties(self):
        self.test_project.findCriticalActivities()

    def test_criticalPath(self):
        self.test_project.criticalPath()

    def test_calc_min_num_worker(self):
        self.test_project.calc_min_num_worker()

    def test_naive_schedule(self):
        self.test_project.naive_schedule()

    def test_createSchedule(self):
        self.test_project.createSchedule()
    '''
