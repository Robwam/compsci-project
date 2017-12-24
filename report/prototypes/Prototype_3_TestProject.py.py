import TestScheduler.mock_data as mock_data

from Scheduler.Models.Project import Project

from nose.tools import assert_equal, assert_raises

class TestProject():
    def __init__(self):
        self.test_project = None

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
