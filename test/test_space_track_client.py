import unittest
import requests
from ..spacetracktool import spacetracktool as st


class TestSpaceTrackClient(unittest.TestCase):
    """ Tests the LteQuery class of the space_track module. """

    def setUp(self):
        self.user = 'user'
        self.passwd = 'pass'
        self.client = st.SpaceTrackClient(self.user, self.passwd)

    def test_init(self):
        self.assertEqual(self.client.username, self.user,
                         'username did not initialize correctly!')
        self.assertEqual(self.client.password, self.passwd,
                         'password did not initialize correctly!')

    def test_tle_query(self):
        with self.assertRaisesRegex(requests.exceptions.HTTPError,
                                    '401 Client Error',
                                    'Unexpected requests error raised!'):
            self.client.tle_query(norad_cat_id=12345)
        self.assertEqual(self.client.print_query(),
                         'https://space-track.org/basicspacedata/query/class/tle/NORAD_CAT_ID/12345/format/json',
                         'tle_query did not update _query correctly!')
