from Scheduler.Models.Event import Event

from nose.tools import assert_equal

# Events connect activities, starting at the source node and ending at the sink node
class MockActivty():
    def __init__(self, name):
        self.name = name

# TODO
# class TestEvent():
#     def test_init(self):
#         e = Event(identifier='A', [MockActivty(name='B'), MockActivty(name='C')])
#         assert_equal(e.__repr__(), 'A [0|0, [B,C]]')
