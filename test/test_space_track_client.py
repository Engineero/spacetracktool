import unittest
import requests
from .. import spacetracktool as st


class TestSpaceTrackClient(unittest.TestCase):
    """ Tests the LteQuery class of the space_track module. """

    def setUp(self):
        self.user = 'user'
        self.passwd = 'pass'
        self.client = st.SpaceTrackClient(self.user, self.passwd)

    def test_init(self):
        self.assertEqual(self.client._username, self.user,
                         'username did not initialize correctly!')
        self.assertEqual(self.client._password, self.passwd,
                         'password did not initialize correctly!')

    def test_tle_query(self):
        with self.assertRaisesRegex(IndexError, 'at least one keyword',
                                    msg='IndexError not raised by tle_query!'):
            self.client.tle_query()
        with self.assertRaisesRegex(KeyError, 'Unexpected argument',
                                    msg='KeyError not raised by tle_query!'):
            self.client.tle_query(not_a_kwarg=True)
        with self.assertRaisesRegex(requests.exceptions.HTTPError,
                                    '401 Client Error',
                                    msg='Unexpected requests error raised!'):
            self.client.tle_query(norad_cat_id=12345)
        query = self.client.print_query()
        self.assertIsInstance(query, str, 'query not of the correct type!')
        self.assertEqual(query,
                         'https://www.space-track.org/basicspacedata/query/class/tle/NORAD_CAT_ID/12345/format/json',
                         'tle_query did not update _query correctly!')

    def test_tle_latest_query(self):
        with self.assertRaisesRegex(IndexError, 'at least one keyword',
                                    msg='IndexError not raised by tle_latest_query!'):
            self.client.tle_latest_query()
        with self.assertRaisesRegex(KeyError, 'Unexpected argument',
                                    msg='KeyError not raised by tle_latest_query!'):
            self.client.tle_latest_query(not_a_kwarg=True)
        with self.assertRaisesRegex(requests.exceptions.HTTPError,
                                    '401 Client Error',
                                    msg='Unexpected requests error raised!'):
            self.client.tle_latest_query(norad_cat_id=12345)

    def test_tle_publish_query(self):
        with self.assertRaisesRegex(IndexError, 'at least one keyword',
                                    msg='IndexError not raised by tle_publish_query!'):
            self.client.tle_publish_query()
        with self.assertRaisesRegex(KeyError, 'Unexpected argument',
                                    msg='KeyError not raised by tle_publish_query!'):
            self.client.tle_publish_query(not_a_kwarg=True)
        with self.assertRaisesRegex(requests.exceptions.HTTPError,
                                    '401 Client Error',
                                    msg='Unexpected requests error raised!'):
            self.client.tle_publish_query(publish_epoch='2018-01-01')

    def test_box_score_query(self):
        with self.assertRaisesRegex(IndexError, 'at least one keyword',
                                    msg='IndexError not raised by box_score_query!'):
            self.client.box_score_query()
        with self.assertRaisesRegex(KeyError, 'Unexpected argument',
                                    msg='KeyError not raised by box_score_query!'):
            self.client.box_score_query(not_a_kwarg=True)
        with self.assertRaisesRegex(requests.exceptions.HTTPError,
                                    '401 Client Error',
                                    msg='Unexpected requests error raised!'):
            self.client.box_score_query(country='usa')

    def test_satcat_query(self):
        with self.assertRaisesRegex(IndexError, 'at least one keyword',
                                    msg='IndexError not raised by satcat_query!'):
            self.client.satcat_query()
        with self.assertRaisesRegex(KeyError, 'Unexpected argument',
                                    msg='KeyError not raised by satcat_query!'):
            self.client.satcat_query(not_a_kwarg=True)
        with self.assertRaisesRegex(requests.exceptions.HTTPError,
                                    '401 Client Error',
                                    msg='Unexpected requests error raised!'):
            self.client.satcat_query(norad_cat_id=12345)

    def test_launch_site_query(self):
        with self.assertRaisesRegex(IndexError, 'at least one keyword',
                                    msg='IndexError not raised by launch_site_query!'):
            self.client.launch_site_query()
        with self.assertRaisesRegex(KeyError, 'Unexpected argument',
                                    msg='KeyError not raised by launch_site_query!'):
            self.client.launch_site_query(not_a_kwarg=True)
        with self.assertRaisesRegex(requests.exceptions.HTTPError,
                                    '401 Client Error',
                                    msg='Unexpected requests error raised!'):
            self.client.launch_site_query(launch_site='FL')

    def test_satcat_change_query(self):
        with self.assertRaisesRegex(IndexError, 'at least one keyword',
                                    msg='IndexError not raised by satcat_change_query!'):
            self.client.satcat_change_query()
        with self.assertRaisesRegex(KeyError, 'Unexpected argument',
                                    msg='KeyError not raised by satcat_change_query!'):
            self.client.satcat_change_query(not_a_kwarg=True)
        with self.assertRaisesRegex(requests.exceptions.HTTPError,
                                    '401 Client Error',
                                    msg='Unexpected requests error raised!'):
            self.client.satcat_change_query(norad_cat_id=12345)

    def test_satcat_debut_query(self):
        with self.assertRaisesRegex(IndexError, 'at least one keyword',
                                    msg='IndexError not raised by satcat_debut_query!'):
            self.client.satcat_debut_query()
        with self.assertRaisesRegex(KeyError, 'Unexpected argument',
                                    msg='KeyError not raised by satcat_debut_query!'):
            self.client.satcat_debut_query(not_a_kwarg=True)
        with self.assertRaisesRegex(requests.exceptions.HTTPError,
                                    '401 Client Error',
                                    msg='Unexpected requests error raised!'):
            self.client.satcat_debut_query(norad_cat_id=12345)

    def test_decay_query(self):
        with self.assertRaisesRegex(IndexError, 'at least one keyword',
                                    msg='IndexError not raised by decay_query!'):
            self.client.decay_query()
        with self.assertRaisesRegex(KeyError, 'Unexpected argument',
                                    msg='KeyError not raised by decay_query!'):
            self.client.decay_query(not_a_kwarg=True)
        with self.assertRaisesRegex(requests.exceptions.HTTPError,
                                    '401 Client Error',
                                    msg='Unexpected requests error raised!'):
            self.client.decay_query(norad_cat_id=12345)

    def test_tip_query(self):
        with self.assertRaisesRegex(IndexError, 'at least one keyword',
                                    msg='IndexError not raised by tip_query!'):
            self.client.tip_query()
        with self.assertRaisesRegex(KeyError, 'Unexpected argument',
                                    msg='KeyError not raised by tip_query!'):
            self.client.tip_query(not_a_kwarg=True)
        with self.assertRaisesRegex(requests.exceptions.HTTPError,
                                    '401 Client Error',
                                    msg='Unexpected requests error raised!'):
            self.client.tip_query(norad_cat_id=12345)

    def test_announcement_query(self):
        with self.assertRaisesRegex(IndexError, 'at least one keyword',
                                    msg='IndexError not raised by announcement_query!'):
            self.client.announcement_query()
        with self.assertRaisesRegex(KeyError, 'Unexpected argument',
                                    msg='KeyError not raised by announcement_query!'):
            self.client.announcement_query(not_a_kwarg=True)
        with self.assertRaisesRegex(requests.exceptions.HTTPError,
                                    '401 Client Error',
                                    msg='Unexpected requests error raised!'):
            self.client.announcement_query(announcement_start='2018-01-01')

    def test_cdm_query(self):
        with self.assertRaisesRegex(IndexError, 'at least one keyword',
                                    msg='IndexError not raised by tle_query!'):
            with self.assertWarnsRegex(Warning, 'not supported',
                                       msg='cdm_query did not raise expected warning!'):
                self.client.cdm_query()

    def test_organization_query(self):
        with self.assertRaisesRegex(IndexError, 'at least one keyword',
                                    msg='IndexError not raised by tle_query!'):
            with self.assertWarnsRegex(Warning, 'not supported',
                                       msg='organization_query did not raise expected warning!'):
                self.client.organization_query()
