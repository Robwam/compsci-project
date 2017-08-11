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

    def test_order_activities(self):
        self.test_project.order_activities()

    def test_calcEarlyTimes(self):
        self.test_project.calcEarlyTimes()

    def test_activitiesFromEvent(self):
        self.test_project.activitiesFromEvent()

    def test_calcLateTimes(self):
        self.test_project.calcLateTimes()

    def test_calcFloats(self):
        self.test_project.calcFloats()

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
    
