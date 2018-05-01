import unittest
from ..spacetracktool import spacetracktool as st
from ..spacetracktool import operations as ops


class TestOperations(unittest.TestCase):
    """ Tests the LteQuery class of the space_track module. """

    def setUp(self):
        self.client = st.SpaceTrackClient('user', 'pass')

    def test_make_range_string(self):
        date_range = ops.make_range_string('2018-01-01', '2018-01-31')
        self.assertEqual(date_range, '2018-01-01--2018-01-31',
                         'date_range was not correct!')
