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
                                    msg='Unexpected requests error raised!'):
            self.client.tle_query(norad_cat_id=12345)
        query = self.client.print_query()
        self.assertIsInstance(query, str, 'query not of the correct type!')
        self.assertEqual(query,
                         'https://space-track.org/basicspacedata/query/class/tle/NORAD_CAT_ID/12345/format/json',
                         'tle_query did not update _query correctly!')

    def test_tle_latest_query(self):
        with self.assertRaisesRegex(NotImplementedError, 'under construction',
                                    msg='tle_latest_query did not say under construction!'):
            self.client.tle_latest_query()

    def test_box_score_query(self):
        with self.assertRaisesRegex(NotImplementedError, 'under construction',
                                    msg='box_score_query did not say under construction!'):
            self.client.box_score_query()

    def test_satcat_query(self):
        with self.assertRaisesRegex(NotImplementedError, 'under construction',
                                    msg='satcat_query did not say under construction!'):
            self.client.satcat_query()

    def test_launch_site_query(self):
        with self.assertRaisesRegex(NotImplementedError, 'under construction',
                                    msg='launch_site_query did not say under construction!'):
            self.client.launch_site_query()

    def test_satcat_change_query(self):
        with self.assertRaisesRegex(NotImplementedError, 'under construction',
                                    msg='satcat_change_query did not say under construction!'):
            self.client.satcat_change_query()

    def test_satcat_debut_query(self):
        with self.assertRaisesRegex(NotImplementedError, 'under construction',
                                    msg='satcat_debut_query did not say under construction!'):
            self.client.satcat_debut_query()

    def test_decay_query(self):
        with self.assertRaisesRegex(NotImplementedError, 'under construction',
                                    msg='decay_query did not say under construction!'):
            self.client.decay_query()

    def test_announcement_query(self):
        with self.assertRaisesRegex(NotImplementedError, 'under construction',
                                    msg='announcement_query did not say under construction!'):
            self.client.announcement_query()

    def test_cdm_query(self):
        with self.assertRaisesRegex(NotImplementedError, 'under construction',
                                    msg='cdm_query did not say under construction!'):
            self.client.cdm_query()

    def test_organization_query(self):
        with self.assertRaisesRegex(NotImplementedError, 'under construction',
                                    msg='organization_query did not say under construction!'):
            self.client.organization_query()
