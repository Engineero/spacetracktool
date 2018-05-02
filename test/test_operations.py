import unittest
from .. import spacetracktool as st
from ..spacetracktool import operations as ops


class TestOperations(unittest.TestCase):
    """ Tests the LteQuery class of the space_track module. """

    def setUp(self):
        self.client = st.SpaceTrackClient('user', 'pass')

    def test_make_range_string(self):
        with self.assertRaisesRegex(ValueError, "if 'equal' is True",
                                    msg='make_range_string raised unexpected error!'):
            ops.make_range_string(equal=True)
        with self.assertRaisesRegex(ValueError, "if 'equal' is False",
                                    msg='make_range_string raised unexpected error!'):
            ops.make_range_string(equal=False)
        num_greater = ops.make_range_string(start=1)
        num_less = ops.make_range_string(end=2)
        date_range = ops.make_range_string('2018-01-01', '2018-01-31')
        date_equal = ops.make_range_string('2018-01-02', '2018-01-03', equal=True)
        date_equal2 = ops.make_range_string(end='2018-01-04', equal=True)
        date_greater = ops.make_range_string('2018-01-05')
        date_less = ops.make_range_string(end='2018-01-06')
        num_greater = ops.make_range_string(start=1)
        num_less = ops.make_range_string(end=2)
        self.assertEqual(date_range, '2018-01-01--2018-01-31',
                         'date_range was not correct!')
        self.assertEqual(date_equal, '2018-01-02',
                         'date_equal was not correct!')
        self.assertEqual(date_equal2, '2018-01-04',
                         'date_equal2 was not correct!')
        self.assertEqual(date_greater, '>2018-01-05',
                         'date_greater was not correct!')
        self.assertEqual(date_less, '<2018-01-06',
                         'date_less was not correct!')
        self.assertEqual(num_greater, '>1',
                         'num_greater was not correct!')
        self.assertEqual(num_less, '<2',
                         'num_less was not correct!')
