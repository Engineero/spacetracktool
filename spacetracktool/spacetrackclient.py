""" Defines the space-track.org query client.

Queries to space-track.org are made by first creating a client instance, and
then calling the appropriate method for your desired query type. Multiple
queries may be created with the same client, but each new query type overwrites
the previous query (cannot run multiple concurrent queries with a singel submit
command).

"""


import warnings
import requests


# pylint: disable=unused-variable
class SpaceTrackClient:
    """ Provides an API for making POST requests to space-track.org

    Args:
        username: your space-track.org username.
        password: the associated password.

    Kwargs:
        fmt: string specifying format for returned message. Can be one of
            'xml', 'json', 'html', 'csv', 'tle', '3le', 'kvn', or None.
            None is the same as 'json'. Default is None.

    Properties:
        result: the result string returned from space-track.org by the last-run
            submit command.

    Examples::

        >> import spacetracktool as st
        >> from spacetracktool import operations as ops
        >> client = SpaceTrackClient(username, password)
        >> result = client.tle_query(norad_cat_id=12345)

        >> date_range = ops.make_range_string('2018-01-01', '2018-01-31')
        >> result = client.tle_query(epoch=date_range)  # throws out previous query!

    """
    _base = 'https://space-track.org'  # base URL for requests
    _login_url = 'https://www.space-track.org/ajaxauth/login'  # login URL
    _logout_url = 'https://www.space-track.org/ajaxauth/logout'
    _null = 'null-val'  # string used by space-track for null values

    def __init__(self, username: str, password: str, fmt: str=None):
        """ Initializes the API.

        Raises:
            ValueError: if provided fmt is not one of the specified options.

        """
        valid_fmt = ['xml', 'json', 'html', 'csv', 'tle', '3le', 'kvn']
        if fmt is not None:
            # pylint: disable=not-callable
            self._fmt = fmt.lower()
            if self._fmt not in valid_fmt:
                raise ValueError("fmt must be one of 'xml', 'json', 'html', \
                                 'csv', 'tle', '3le', 'kvn', or None.")
        else:
            self._fmt = 'json'
        self.username = username
        self.password = password
        self._query = []  # placeholder for our query string
        self.result = None  # placeholder for the query result

    def _logout(self) -> requests.models.Response:
        """ Logs out of the space-track.org session.

        Returns:
            Response from space-track.org

        """
        res = requests.post(self.logout_url)
        if not res.ok:
            print('Error logging out! Status code {}'.format(res.status_code))
        return res

    def _basic(self):
        """ Adds 'basicspacedata' to the query. """
        self._query = [self._base, 'basicspacedata']

    def _expanded(self):
        """ Adds 'expandedspacedata' to the query. """
        self._query = [self._base, 'expandedspacedata']

    def _start_query(self):
        """ Builds the start of a basic space data query. """
        self._basic()  # restarts the query string
        self._query.append('query')

    def _start_expanded_query(self):
        """ Builds the start of an expanded space data query. """
        self._expanded()  # restarts the query string
        self._query.append('query')

    def _compile_query(self) -> str:
        """ Compiles the query (list of strings) into a '/'-separated string.

        Returns:
            The query string with each element separated by a forward-slash.

        """
        if self._fmt not in self._query:
            self._query.extend(['format', self._fmt])
        return '/'.join(self._query)

    def print_query(self):
        """ Prints the query to the screen.

        Note that at this stage the format string has not been applied to the
        query. This string gets applied at the very end prior to submitting the
        POST request.

        """
        query_string = '/'.join(self._query)
        print('/'.join(self._query))
        return query_string

    def submit(self) -> requests.models.Response:
        """ Submits the generated query to space-track.org.

        Returns:
            Response from space-track.org

        """
        payload = {'identity': self.username,
                   'password': self.password,
                   'query': self._compile_query()}
        self.result = requests.post(self.login_url, data=payload)
        if not self.result.ok:
            print('Error posting request! Status code {}'.format(
                self.result.status_code))
            # pylint: disable=not-callable
            self.result.raise_for_status()  # raise HTTP error
        # self._logout()
        return self.result

    def _value_query(self, key: str, value: str):
        """ Specifies a "value equals ___" query.

        Args:
            key: the key to add to the query string
            value: the value to search for

        Raises:
            ValueError: if key or value are not of type string and cannot be
                coerced into a string.

        """
        if not isinstance(key, str):
            try:
                key = str(key)
            except Exception as excep:
                print(excep)
                raise ValueError('key argument must be a string or',
                                 'coercable to string!')
        if not isinstance(value, str):
            try:
                value = str(value)
            except Exception as excep:
                print(excep)
                raise ValueError('value argument must be a string or',
                                 'coercable to string!')
        self._query.extend([key, value])

    def _make_query(self, key_list: list, kwargs: dict):
        """ Forms a query using expected keys and provided keyword args.

        Args:
            key_list: list of expected, possible keys.
            kwargs: dictionary of provided keyword args.

        Raises:
            KeyError: if a key is given that is not in the key list

        """
        # pylint: disable=not-callable
        for k in kwargs.keys():
            if k not in key_list:
                err_msg = ('Unexpected argument {} given! '.format(k) +
                           'If you believe this is a valid key, please ' +
                           'submit a pull request or open an issue on GitHub.')
                raise KeyError(err_msg)
        for key in key_list:
            # pylint: disable=not-callable
            if key in kwargs.keys():
                self._value_query(key.upper(), kwargs.pop(key))

    def tle_query(self, **kwargs):
        """ Initiates a TLE query request.

        Any number of keyword arguments that are defined by the space-track.org
        API may be provided. Single value arguments are easy and should be
        passed a string or an object that can be coerced to a string::

            >> import spacetracktool as st
            >> query = st.SpaceTrackClient('username', 'password')
            >> result = query.tle_query(norad_cat_id=12345)

        Range arugment strings should be built with the
        spacetracktool.operations.make_range_string method. For example, to
        provide a date range to the `epoch` argument::

            >> import spacetracktool as st
            >> from spacetracktool import operations as ops
            >> date_range = ops.make_range_string('2018-01-01', '2018-01-31')
            >> query = st.SpaceTrackClient('username', 'password')
            >> result = query.tle_query(epoch=date_range)

        Keyword Args:
            comment (str): TODO
            originator (str): TODO
            norad_cat_id (int, str): The norad catalog ID of a satellite.
                Should be a single value.
            object_name (str): The name string associated with an object.
                Should be a single value.
            object_type (int, str): The catalog object type. Should be a single
                value.
            classification_type (int, str): TODO
            intldes (int, str):
            epoch (str): The epoch date or date range in which to search. May
                be a single value or a range. Dates should be specified in
                ether of the followingthe formats::

                    'YYYY-MM-DD HH:mm:ss'
                    'YYYY-MM-DD'

            epoch_microseconds (str): TODO
            mean_motion (float, str): The mean motion to search in revolutions
                per day. May be a single value or a range.
            eccentricity (float, str): The eccentricity to search. May be a
                single value or a range.
            inclination (float, str): The inclination to search in degrees. May
                be a single value or a range.
            ra_of_asc_node (float, str): The right-ascension of the ascending
                node to search in degrees. May be a single value or a range.
            arg_of_pericenter (float, str): The argument of the pericenter to
                search. May be a single value or a range.
            mean_anomaly (float, str): The mean anomaly to search. May be a
                single value or a range.
            ephemeris_type (int, str): TODO
            element_set_no (int, str): The element set number to search. May be
                a single value or a range.
            rev_at_epoch (float, str): The revolution at epoch to search. May
                be a single value or a range.
            bstar (float, str): The b-star drag coefficient to search. May be a
                single value or a range.
            mean_motion_dot (float, str): The first derivative of the mean
                motion with respect to time. May be a single value or a range.
            mean_motion_ddot (float, str): The second derivative of the mean
                motion with respect to time. May be a single value or a range.
            file (int, str): TODO
            tle_line0 (str): The first line of a three-line element set.
            tle_line1 (str): The second line of a three-line element set or
                first line of a two-line element set.
            tle_line2 (str): The third line of a three-line element set or
                second line of a two-line element set.
            object_id (int, str): maybe synonomous with norad_cat_id?
            object_number (int, str): synonomous with norad_cat_id.
            semimajor_axis (float, str): The semimajor axis in Earth radii. May
                be a single value or a range.
            period (float, str): The orbital period in days. May be single
                value or a range.
            apogee (float, str): The radius when furthest from the Earth. May
                be a single value or a range.
            perigee (float, str): The radius when furthest from the Earth. May
                be a single value or a range.

        Returns:
            The result of the query to space-track.org

        Raises:
            IndexError: if no keyword arguments are provided
            KeyError: if any provided key is not in the expected argument list

        """
        if len(kwargs) == 0:
            raise IndexError('Must supply at least one keyword argument!')
        key_list = ['comment', 'originator', 'norad_cat_id', 'object_name',
                    'object_type', 'classification_type', 'intldes', 'epoch',
                    'epoch_microseconds', 'mean_motion', 'eccentricity',
                    'inclination', 'ra_of_asc_node', 'arg_of_pericenter',
                    'mean_anomaly', 'ephemeris_type', 'element_set_no',
                    'rev_at_epoch', 'bstar', 'mean_motion_dot',
                    'mean_motion_ddot', 'file', 'tle_line0', 'tle_line1',
                    'tle_line2', 'object_id', 'object_number',
                    'semimajor_axis', 'period', 'apogee', 'perigee']
        self._start_query()
        self._query.extend(['class', 'tle'])
        self._make_query(key_list, kwargs)
        return self.submit()

    def tle_latest_query(self, **kwargs):
        """ Initiates a TLE_latest query request.

        Any number of keyword arguments that are defined by the space-track.org
        API may be provided. Single value arguments are easy and should be
        passed a string or an object that can be coerced to a string::

            >> import spacetracktool as st
            >> query = st.SpaceTrackClient('username', 'password')
            >> result = query.tle_latest_query(norad_cat_id=12345)

        Range arugment strings should be built with the
        spacetracktool.operations.make_range_string method. For example, to
        provide a date range to the `epoch` argument::

            >> import spacetracktool as st
            >> from spacetracktool import operations as ops
            >> date_range = ops.make_range_string('2018-01-01', '2018-01-31')
            >> query = st.SpaceTrackClient('username', 'password')
            >> result = query.tle_latest_query(epoch=date_range)

        Keyword Args:
            ordinal (int, str): TODO
            comment (str): TODO
            originator (str): TODO
            norad_cat_id (int, str): The norad catalog ID of a satellite.
                Should be a single value.
            object_name (str): The name string associated with an object.
                Should be a single value.
            object_type (int, str): The catalog object type. Should be a single
                value.
            classification_type (int, str): TODO
            intldes (int, str):
            epoch (str): The epoch date or date range in which to search. May
                be a single value or a range. Dates should be specified in
                ether of the followingthe formats::

                    'YYYY-MM-DD HH:mm:ss'
                    'YYYY-MM-DD'

            epoch_microseconds (str): TODO
            mean_motion (float, str): The mean motion to search in revolutions
                per day. May be a single value or a range.
            eccentricity (float, str): The eccentricity to search. May be a
                single value or a range.
            inclination (float, str): The inclination to search in degrees. May
                be a single value or a range.
            ra_of_asc_node (float, str): The right-ascension of the ascending
                node to search in degrees. May be a single value or a range.
            arg_of_pericenter (float, str): The argument of the pericenter to
                search. May be a single value or a range.
            mean_anomaly (float, str): The mean anomaly to search. May be a
                single value or a range.
            ephemeris_type (int, str): TODO
            element_set_no (int, str): The element set number to search. Should
                be a single value.
            rev_at_epoch (float, str): The revolution at epoch to search. May
                be a single value or a range.
            bstar (float, str): The b-star drag coefficient to search. May be a
                single value or a range.
            mean_motion_dot (float, str): The first derivative of the mean
                motion with respect to time. May be a single value or a range.
            mean_motion_ddot (float, str): The second derivative of the mean
                motion with respect to time. May be a single value or a range.
            file (int, str): TODO
            tle_line0 (str): The first line of a three-line element set.
            tle_line1 (str): The second line of a three-line element set or
                first line of a two-line element set.
            tle_line2 (str): The third line of a three-line element set or
                second line of a two-line element set.
            object_id (str): TODO
            object_number (int, str): synonomous with norad_cat_id.
            semimajor_axis (float, str): The semimajor axis in Earth radii. May
                be a single value or a range.
            period (float, str): The orbital period in days. May be single
                value or a range.
            apogee (float, str): The radius when furthest from the Earth. May
                be a single value or a range.
            perigee (float, str): The radius when furthest from the Earth. May
                be a single value or a range.

        Returns:
            The result of the query to space-track.org

        Raises:
            IndexError: if no keyword arguments are provided
            KeyError: if any provided key is not in the expected argument list

        """
        if len(kwargs) == 0:
            raise IndexError('Must supply at least one keyword argument!')
        key_list = ['ordinal', 'comment', 'originator', 'norad_cat_id',
                    'object_name', 'object_type', 'classification_type',
                    'intldes', 'epoch', 'epoch_microseconds' 'mean_motion',
                    'eccentricity', 'inclination', 'ra_of_asc_node',
                    'arg_of_pericenter', 'mean_anomaly', 'ephemeris_type',
                    'element_set_no', 'rev_at_epoch', 'bstar',
                    'mean_motion_dot', 'mean_motion_ddot', 'file', 'tle_line0',
                    'tle_line1', 'tle_line2', 'semimajor_axis', 'period',
                    'apogee', 'perigee']
        self._start_query()
        self._query.extend(['class', 'tle_latest'])
        self._make_query(key_list, kwargs)
        return self.submit()

    def tle_publish_query(self, **kwargs):
        """ Initiates a tle_publish query request.

        Returns:
            The result of the query to space-track.org

        Raises:
            IndexError: if no keyword arguments are provided
            KeyError: if any provided key is not in the expected argument list

        """
        if len(kwargs) == 0:
            raise IndexError('Must supply at least one keyword argument!')
        key_list = ['publish_epoch', 'tle_line1', 'tle_line2']
        self._start_query()
        self._query.extend(['class', 'tle_publish'])
        self._make_query(key_list, kwargs)
        return self.submit()

    def box_score_query(self, **kwargs):
        """ Initiates a boxscore query request.

        Returns:
            The result of the query to space-track.org

        Raises:
            IndexError: if no keyword arguments are provided
            KeyError: if any provided key is not in the expected argument list

        """
        if len(kwargs) == 0:
            raise IndexError('Must supply at least one keyword argument!')
        key_list = ['country', 'spadoc_cd', 'orbital_tba',
                    'orbital_payload_count', 'orbital_rocket_body_count',
                    'orbital_debris_count', 'orbital_total_count',
                    'decayed_payload_count', 'decayed_rocket_body_count',
                    'decayed_debris_count', 'decayed_total_count',
                    'country_total']
        self._start_query()
        self._query.extend(['class', 'boxscore'])
        self._make_query(key_list, kwargs)
        return self.submit()

    def satcat_query(self, **kwargs):
        """ Initiates a satcat query request.

        Returns:
            The result of the query to space-track.org

        Raises:
            IndexError: if no keyword arguments are provided
            KeyError: if any provided key is not in the expected argument list

        """
        if len(kwargs) == 0:
            raise IndexError('Must supply at least one keyword argument!')
        key_list = ['intldes', 'norad_cat_id', 'object_type', 'satname',
                    'country', 'launch', 'site', 'decay', 'period',
                    'inclination', 'apogee', 'perigee', 'comment',
                    'commentcode', 'rcsvalue', 'rcs_size', 'file',
                    'launch_year', 'launch_num', 'launch_piece', 'current',
                    'object_name', 'object_id', 'object_number']
        self._start_query()
        self._query.extend(['class', 'satcat'])
        self._make_query(key_list, kwargs)
        return self.submit()

    def launch_site_query(self, **kwargs):
        """ Initiates a launch_site request.

        Returns:
            The result of the query to space-track.org

        Raises:
            IndexError: if no keyword arguments are provided
            KeyError: if any provided key is not in the expected argument list

        """
        if len(kwargs) == 0:
            raise IndexError('Must supply at least one keyword argument!')
        key_list = ['site_code', 'launch_site']
        self._start_query()
        self._query.extend(['class', 'launch_site'])
        self._make_query(key_list, kwargs)
        return self.submit()

    def satcat_change_query(self, **kwargs):
        """ Initiates a satcat_change request.

        Returns:
            The result of the query to space-track.org

        Raises:
            IndexError: if no keyword arguments are provided
            KeyError: if any provided key is not in the expected argument list

        """
        if len(kwargs) == 0:
            raise IndexError('Must supply at least one keyword argument!')
        key_list = ['norad_cat_id', 'object_number', 'current_name',
                    'previous_name', 'current_intldes', 'previous_intldes',
                    'current_country', 'previous_country', 'current_launch',
                    'previous_launch', 'current_decay', 'previous_decay',
                    'change_made']
        self._start_query()
        self._query.extend(['class', 'satcat_change'])
        self._make_query(key_list, kwargs)
        return self.submit()

    def satcat_debut_query(self, **kwargs):
        """ Initiates a satcat_debut request.

        Returns:
            The result of the query to space-track.org

        Raises:
            IndexError: if no keyword arguments are provided
            KeyError: if any provided key is not in the expected argument list

        """
        if len(kwargs) == 0:
            raise IndexError('Must supply at least one keyword argument!')
        key_list = ['intldes', 'norad_cat_id', 'satname', 'debut', 'country',
                    'launch', 'site', 'decay', 'period', 'inclination',
                    'apogee', 'perigee', 'comment', 'commentcode', 'rcsvalue',
                    'rcs_size', 'launch_piece', 'current', 'object_name',
                    'object_id', 'object_number']
        self._start_query()
        self._query.extend(['class', 'satcat_debut'])
        self._make_query(key_list, kwargs)
        return self.submit()

    def decay_query(self, **kwargs):
        """ Initiates a decay request.

        Note that if the 'precedence' argument is not provided, it will default
        to a precedence of 2, which means messages that specifically announce
        that the object has decayed.

        Returns:
            The result of the query to space-track.org

        Raises:
            IndexError: if no keyword arguments are provided
            KeyError: if any provided key is not in the expected argument list

        """
        if len(kwargs) == 0:
            raise IndexError('Must supply at least one keyword argument!')
        key_list = ['norad_cat_id', 'object_number', 'object_name', 'intldes',
                    'object_id', 'rcs', 'rcs_size', 'country', 'msg_epoch',
                    'decay_epoch', 'source', 'msg_type', 'precedence']
        if 'precedence' not in list(kwargs.keys()):
            kwargs['precedence'] = 2  # default to decay announcements
        self._start_query()
        self._query.extend(['class', 'decay'])
        self._make_query(key_list, kwargs)
        return self.submit()

    def tip_query(self, **kwargs):
        """ Initiates a tracking and impact prediction (TIP) request.

        Returns:
            The result of the query to space-track.org

        Raises:
            IndexError: if no keyword arguments are provided
            KeyError: if any provided key is not in the expected argument list

        """
        if len(kwargs) == 0:
            raise IndexError('Must supply at least one keyword argument!')
        key_list = ['norad_cat_id', 'msg_epoch', 'insert_epoch', 'decay_epoch',
                    'window', 'rev', 'direction', 'lat', 'lon', 'incl',
                    'next_report', 'id', 'high_interest', 'object_number']
        self._start_query()
        self._query.extend(['class', 'tip'])
        self._make_query(key_list, kwargs)
        return self.submit()

    def announcement_query(self, **kwargs):
        """ Initiates a announcement request.

        Returns:
            The result of the query to space-track.org

        Raises:
            IndexError: if no keyword arguments are provided
            KeyError: if any provided key is not in the expected argument list

        """
        if len(kwargs) == 0:
            raise IndexError('Must supply at least one keyword argument!')
        key_list = ['announcement_type', 'announcement_text',
                    'announcement_start', 'announcement_end']
        self._start_query()
        self._query.extend(['class', 'announcement'])
        self._make_query(key_list, kwargs)
        return self.submit()

    def cdm_query(self, **kwargs):
        """ Initiates a cdm request.

        Returns:
            The result of the query to space-track.org

        Raises:
            IndexError: if no keyword arguments are provided
            KeyError: if any provided key is not in the expected argument list

        """
        warnings.warn('Expanded space data queries are not supported at this time.',
                      Warning)
        if len(kwargs) == 0:
            raise IndexError('Must supply at least one keyword argument!')
        key_list = ['constellation', 'cdm_id', 'filename', 'insert_epoch',
                    'ccsds_cdm_vers', 'creation_date', 'creation_date_fraction',
                    'originator', 'message_for', 'message_id',
                    'comment_emergency_reportable', 'tca', 'tca_fraction',
                    'miss_distance', 'miss_distance_unit', 'relative_speed',
                    'relative_speed_unit', 'relative_position_r',
                    'relative_position_r_unit', 'relative_position_t',
                    'relative_position_t_unit', 'relative_position_n',
                    'relative_position_n_unit', 'relative_velocity_r',
                    'relative_velocity_r_unit', 'relative_velocity_t',
                    'relative_velocity_t_unit', 'relative_velocity_n',
                    'relative_velocity_n_unit', 'collision_probability',
                    'collision_probability_method', 'sat1_object',
                    'sat1_object_designator', 'sat1_catalog_name',
                    'sat1_object_name', 'sat1_international_designator',
                    'sat1_object_type', 'sat1_operator_contact_position',
                    'sat1_operator_organization', 'sat1_operator_phone',
                    'sat1_operator_email', 'sat1_ephemeris_name',
                    'sat1_covariance_method', 'sat1_maneuverable',
                    'sat1_ref_frame', 'sat1_gravity_model',
                    'sat1_atmospheric_model', 'sat1_n_body_perturbations',
                    'sat1_solar_rad_pressure', 'sat1_earth_tides',
                    'sat1_intrack_thrust', 'sat1_time_lastob_start',
                    'sat1_time_lastob_start_fraction', 'sat1_time_lastob_end',
                    'sat1_time_lastob_end_fraction', 'sat1_recommended_od_span',
                    'sat1_recommended_od_span_unit', 'sat1_actual_od_span',
                    'sat1_actual_od_span_unit', 'sat1_obs_available',
                    'sat1_obs_used', 'sat1_residuals_accepted',
                    'sat1_residuals_accepted_unit', 'sat1_weighted_rms',
                    'sat1_comment_apogee', 'sat1_comment_perigee',
                    'sat1_comment_inclination', 'sat1_area_pc',
                    'sat1_area_pc_unit', 'sat1_cd_area_over_mass',
                    'sat1_cd_area_over_mass_unit', 'sat1_cr_area_over_mass',
                    'sat1_cr_area_over_mass_unit', 'sat1_thrust_acceleration',
                    'sat1_thrust_acceleration_unit', 'sat1_sedr',
                    'sat1_sedr_unit', 'sat1_x', 'sat1_x_unit', 'sat1_y',
                    'sat1_y_unit', 'sat1_z', 'sat1_z_unit', 'sat1_x_dot',
                    'sat1_x_dot_unit', 'sat1_y_dot', 'sat1_y_dot_unit',
                    'sat1_z_dot', 'sat1_z_dot_unit', 'sat1_cr_r',
                    'sat1_cr_r_unit', 'sat1_ct_r', 'sat1_ct_r_unit',
                    'sat1_ct_t', 'sat1_ct_t_unit', 'sat1_cn_r',
                    'sat1_cn_r_unit', 'sat1_cn_t', 'sat1_cn_t_unit',
                    'sat1_cn_n', 'sat1_cn_n_unit', 'sat1_crdot_r',
                    'sat1_crdot_r_unit', 'sat1_crdot_t', 'sat1_crdot_t_unit',
                    'sat1_crdot_n', 'sat1_crdot_n_unit', 'sat1_crdot_rdot',
                    'sat1_crdot_rdot_unit', 'sat1_ctdot_r',
                    'sat1_ctdot_r_unit', 'sat1_ctdot_t', 'sat1_ctdot_t_unit',
                    'sat1_ctdot_n', 'sat1_ctdot_n_unit', 'sat1_ctdot_rdot',
                    'sat1_ctdot_rdot_unit', 'sat1_ctdot_tdot',
                    'sat1_ctdot_tdot_unit', 'sat1_cndot_r',
                    'sat1_cndot_r_unit', 'sat1_cndot_t', 'sat1_cndot_t_unit',
                    'sat1_cndot_n', 'sat1_cndot_n_unit', 'sat1_cndot_rdot',
                    'sat1_cndot_rdot_unit', 'sat1_cndot_tdot',
                    'sat1_cndot_tdot_unit', 'sat1_cndot_ndot',
                    'sat1_cndot_ndot_unit', 'sat1_cdrg_r',
                    'sat1_cdrg_r_unit', 'sat1_cdrg_t', 'sat1_cdrg_t_unit',
                    'sat1_cdrg_n', 'sat1_cdrg_n_unit', 'sat1_cdrg_rdot',
                    'sat1_cdrg_rdot_unit', 'sat1_cdrg_tdot',
                    'sat1_cdrg_tdot_unit', 'sat1_cdrg_ndot',
                    'sat1_cdrg_ndot_unit', 'sat1_cdrg_drg',
                    'sat1_cdrg_drg_unit', 'sat1_csrp_r',
                    'sat1_csrp_r_unit', 'sat1_csrp_t', 'sat1_csrp_t_unit',
                    'sat1_csrp_n', 'sat1_csrp_n_unit', 'sat1_csrp_rdot',
                    'sat1_csrp_rdot_unit', 'sat1_csrp_tdot',
                    'sat1_csrp_tdot_unit', 'sat1_csrp_ndot',
                    'sat1_csrp_ndot_unit', 'sat1_csrp_drg',
                    'sat1_csrp_drg_unit', 'sat1_csrp_srp', 'sat1_csrp_srp_unit',
                    'sat2_object', 'sat2_object_designator',
                    'sat2_catalog_name', 'sat2_object_name',
                    'sat2_international_designator',
                    'sat2_object_type', 'sat2_operator_contact_position',
                    'sat2_operator_organization', 'sat2_operator_phone',
                    'sat2_operator_email', 'sat2_ephemeris_name',
                    'sat2_covariance_method', 'sat2_maneuverable',
                    'sat2_ref_frame', 'sat2_gravity_model',
                    'sat2_atmospheric_model', 'sat2_n_body_perturbations',
                    'sat2_solar_rad_pressure', 'sat2_earth_tides',
                    'sat2_intrack_thrust', 'sat2_time_lastob_start',
                    'sat2_time_lastob_start_fraction', 'sat2_time_lastob_end',
                    'sat2_time_lastob_end_fraction', 'sat2_recommended_od_span',
                    'sat2_recommended_od_span_unit', 'sat2_actual_od_span',
                    'sat2_actual_od_span_unit', 'sat2_obs_available',
                    'sat2_obs_used', 'sat2_residuals_accepted',
                    'sat2_residuals_accepted_unit', 'sat2_weighted_rms',
                    'sat2_comment_apogee', 'sat2_comment_perigee',
                    'sat2_comment_inclination', 'sat2_area_pc',
                    'sat2_area_pc_unit', 'sat2_cd_area_over_mass',
                    'sat2_cd_area_over_mass_unit', 'sat2_cr_area_over_mass',
                    'sat2_cr_area_over_mass_unit', 'sat2_thrust_acceleration',
                    'sat2_thrust_acceleration_unit', 'sat2_sedr',
                    'sat2_sedr_unit', 'sat2_x', 'sat2_x_unit', 'sat2_y',
                    'sat2_y_unit', 'sat2_z', 'sat2_z_unit', 'sat2_x_dot',
                    'sat2_x_dot_unit', 'sat2_y_dot', 'sat2_y_dot_unit',
                    'sat2_z_dot', 'sat2_z_dot_unit', 'sat2_cr_r',
                    'sat2_cr_r_unit', 'sat2_ct_r', 'sat2_ct_r_unit',
                    'sat2_ct_t', 'sat2_ct_t_unit', 'sat2_cn_r',
                    'sat2_cn_r_unit', 'sat2_cn_t', 'sat2_cn_t_unit',
                    'sat2_cn_n', 'sat2_cn_n_unit', 'sat2_crdot_r',
                    'sat2_crdot_r_unit', 'sat2_crdot_t', 'sat2_crdot_t_unit',
                    'sat2_crdot_n', 'sat2_crdot_n_unit', 'sat2_crdot_rdot',
                    'sat2_crdot_rdot_unit', 'sat2_ctdot_r',
                    'sat2_ctdot_r_unit', 'sat2_ctdot_t', 'sat2_ctdot_t_unit',
                    'sat2_ctdot_n', 'sat2_ctdot_n_unit', 'sat2_ctdot_rdot',
                    'sat2_ctdot_rdot_unit', 'sat2_ctdot_tdot',
                    'sat2_ctdot_tdot_unit', 'sat2_cndot_r',
                    'sat2_cndot_r_unit', 'sat2_cndot_t', 'sat2_cndot_t_unit',
                    'sat2_cndot_n', 'sat2_cndot_n_unit', 'sat2_cndot_rdot',
                    'sat2_cndot_rdot_unit', 'sat2_cndot_tdot',
                    'sat2_cndot_tdot_unit', 'sat2_cndot_ndot',
                    'sat2_cndot_ndot_unit', 'sat2_cdrg_r',
                    'sat2_cdrg_r_unit', 'sat2_cdrg_t', 'sat2_cdrg_t_unit',
                    'sat2_cdrg_n', 'sat2_cdrg_n_unit', 'sat2_cdrg_rdot',
                    'sat2_cdrg_rdot_unit', 'sat2_cdrg_tdot',
                    'sat2_cdrg_tdot_unit', 'sat2_cdrg_ndot',
                    'sat2_cdrg_ndot_unit', 'sat2_cdrg_drg',
                    'sat2_cdrg_drg_unit', 'sat2_csrp_r',
                    'sat2_csrp_r_unit', 'sat2_csrp_t', 'sat2_csrp_t_unit',
                    'sat2_csrp_n', 'sat2_csrp_n_unit', 'sat2_csrp_rdot',
                    'sat2_csrp_rdot_unit', 'sat2_csrp_tdot',
                    'sat2_csrp_tdot_unit', 'sat2_csrp_ndot',
                    'sat2_csrp_ndot_unit', 'sat2_csrp_drg',
                    'sat2_csrp_drg_unit', 'sat2_csrp_srp', 'sat2_csrp_srp_unit',
                    'gid']
        self._start_expanded_query()
        self._query.extend(['class', 'cdm'])
        self._make_query(key_list, kwargs)
        return self.submit()

    def organization_query(self, **kwargs):
        """ Initiates a organization request.

        Returns:
            The result of the query to space-track.org

        Raises:
            IndexError: if no keyword arguments are provided
            KeyError: if any provided key is not in the expected argument list

        """
        warnings.warn('Expanded space data queries are not supported at this time.',
                      Warning)
        if len(kwargs) == 0:
            raise IndexError('Must supply at least one keyword argument!')
        key_list = ['gid', 'org_name', 'constellation', 'info_id', 'info_type',
                    'info_label', 'info_value', 'info_modified', 'object_count',
                    'object']
        self._start_expanded_query()
        self._query.extend(['class', 'organization'])
        self._make_query(key_list, kwargs)
        return self.submit()

    @property
    def base(self):
        """ Returns URL base string. """
        return type(self)._base

    @property
    def login_url(self):
        """ Returns login URL string. """
        return type(self)._login_url

    @property
    def logout_url(self):
        """ Returns logout URL string. """
        return type(self)._logout_url

    @property
    def null(self):
        """ Returns space-track.org's null string. """
        return type(self)._null
