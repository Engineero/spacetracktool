import unittest
from .... import space_track as st


class TestLteQuery(unittest.TestCase):
    """ Tests the LteQuery class of the space_track module. """

    def test_init(self):
        lte_query = st.LteQuery('user', 'pass')
        self.assertEqual(lte_query.print_query(),
                         'https://space-track.org/basicspacedata/query/class/tle',
                         'Query did not initialize correctly.')


if __name__ == '__main__':
    unittest.main()
