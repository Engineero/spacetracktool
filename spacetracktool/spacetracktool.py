""" Defines the space-track.org query client.

Queries to space-track.org are made by first creating a client instance, and
then calling the appropriate method for your desired query type. Multiple
queries may be created with the same client, but each new query type overwrites
the previous query (cannot run multiple concurrent queries with a singel submit
command).

"""


import requests
import .operations as ops


class SpaceTrackClient():
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
        >> import spacetracktool.operations as ops
        >> client = SpaceTrackClient(username, password)
        >> client.tle_query(norad_cat_id=12345)
        >> result = client.submit()
    
        >> date_range = ops.make_range_string('2018-01-01', '2018-01-31')
        >> client.tle_query(epoch=date_range)  # throws out previous query!
        >> new_result = client.submit()

    """
    _base = 'https://space-track.org/'  # base URL for requests
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
            if fmt.lower() not in valid_fmt:
                raise ValueError("fmt must be one of 'xml', 'json', 'html', \
                                 'csv', 'tle', '3le', 'kvn', or None.")
        else:
            fmt = 'json'
        self._fmt = fmt.lower()
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
        self._query.append('basicspacedata')

    def _start_query(self):
        """ Builds the start of a query. """
        self._query = []  # start from scratch
        self._basic()
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
        print('/'.join(self._query))

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
        self._logout()
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
            except Exception as e:
                print(e)
                raise ValueError('key argument must be a string or',
                                 'coercable to string!')
        if not isinstance(value: str):
            try:
                value = str(value)
            except Exception as e:
                print(e)
                raise ValueError('value argument must be a string or',
                                 'coercable to string!')
        self._query.extend(key, id_number)

    def tle_query(self, **kwargs):
        """ Initiates a TLE query request.
        
        Any number of keyword arguments that are defined by the space-track.org
        API may be provided. Single value arguments are easy and should be
        passed a string or an object that can be coerced to a string::

            >> import spacetracktool as st
            >> query = st.SpaceTrackClient(username, password)
            >> query.tle_query(norad_cat_id=12345)
            >> result = query.submit()

        Range arugment strings should be built with the
        spacetracktool.operations.make_range_string method. For example, to
        provide a date range to the `epoch` argument::

            >> import spacetracktool as st
            >> import spacetracktool.operations as ops
            >> date_range = ops.make_range_string('2018-01-01', '2018-01-31')
            >> query = st.SpaceTrackClient(username, password)
            >> query.tle_query(epoch=date_range)
            >> result = query.submit()

        Keyword Args:
            norad_cat_id: int or str
                The norad catalog ID of a satellite. Should be a single value.

            object_name: str
                The name string associated with an object. Should be a single
                value.

            object_type: int or str
                The catalog object type. Should be a single value.

            epoch: str
                The epoch date or date range in which to search. May be a single
                value or a range. Dates should be specified in ether of the
                followingthe formats::

                    'YYYY-MM-DD HH:mm:ss'
                    'YYYY-MM-DD'

            mean_motion: float or str
                The mean motion to search in revolutions per day. May be a
                single value or a range.

            eccentricity: float or str
                The eccentricity to search. May be a single value or a range.

            inclination: float or str
                The inclination to search in degrees. May be a single value or
                a range.

            ra_of_asc_node: float or str
                The right-ascension of the ascending node to search in degrees.
                May be a single value or a range.

            arg_of_pericenter: float or str
                The argument of the pericenter to search. May be a single value
                or a range.

            mean_anomaly: float or str
                The mean anomaly to search. May be a single value or a range.

            element_set_no: int or str
                The element set number to search. Should be a single value.

            rev_at_epoch: float or str
                The revolution at epoch to search. May be a single value or a
                range.

            bstar: float or str
                The b-star drag coefficient to search. May be a single value
                or a range.

            mean_motion_dot: float or str
                The first derivative of the mean motion with respect to time.
                May be a single value or a range.

            mean_motion_ddot: float or str
                The second derivative of the mean motion with respect to time.
                May be a single value or a range.

            semimajor_axis: float or str
                The semimajor axis in Earth radii. May be a single value or a
                range.

            period: float or str
                The orbital period in days. May be single value or a range.

            apogee: float or str
                The radius when furthest from the Earth. May be a single value
                or a range.

            perigee: float or str
                The radius when furthest from the Earth. May be a single value
                or a range.

        Returns:
            The result of the query to space-track.org

        Raises:
            IndexError: if no keyword arguments are provided
        
        """
        if len(kwargs) == 0:
            raise IndexError('Must supply at least one keyword argument!')
        key_list = ['norad_cat_id', 'object_name', 'object_type', 'epoch',
                    'mean_motion', 'eccentricity', 'inclination',
                    'ra_of_asc_node', 'arg_of_pericenter', 'mean_anomaly',
                    'element_set_no', 'rev_at_epoch', 'bstar',
                    'mean_motion_dot', 'mean_motion_ddot', 'semimajor_axis',
                    'period', 'apogee', 'perigee']
        self._start_query()
        self._query.extend('class', 'tle')
        for key in key_list:
            if key in kwargs.keys():
                self._value_query(key.upper(), kwargs.pop(key))
        return self.submit()

    def tle_latest_query(self):
        """ Initiates a TLE_latest query request. """
        raise NotImplementedError('This method is under construction.',
                                  "If you'd like to help, please submit a pull request!") 
        self._start_query()
        self._query.extend('class', 'tle_latest')
        return self.submit()

    def box_score_query(self):
        """ Initiates a boxscore query request. """
        raise NotImplementedError('This method is under construction.',
                                  "If you'd like to help, please submit a pull request!") 
        self._start_query()
        self._query.extend('class', 'boxscore')
        return self.submit()

    def satcat_query(self):
        """ Initiates a satcat query request. """
        self._start_query()
        self._query.extend('class', 'satcat')
        return self.submit()

    def launch_site_query(self):
        """ Initiates a launch_site request. """
        raise NotImplementedError('This method is under construction.',
                                  "If you'd like to help, please submit a pull request!") 
        self._start_query()
        self._query.extend('class', 'launch_site')
        return self.submit()

    def satcat_change_query(self):
        """ Initiates a satcat_change request. """
        raise NotImplementedError('This method is under construction.',
                                  "If you'd like to help, please submit a pull request!") 
        self._start_query()
        self._query.extend('class', 'satcat_change')
        return self.submit()

    def satcat_debut_query(self):
        """ Initiates a satcat_debut request. """
        raise NotImplementedError('This method is under construction.',
                                  "If you'd like to help, please submit a pull request!")
        self._start_query()
        self._query.extend('class', 'satcat_debut')
        return self.submit()

    def decay_query(self):
        """ Initiates a decay request. """
        raise NotImplementedError('This method is under construction.',
                                  "If you'd like to help, please submit a pull request!")
        self._start_query()
        self._query.extend('class', 'decay')
        return self.submit()

    def announcement_query(self):
        """ Initiates a announcement request. """
        raise NotImplementedError('This method is under construction.',
                                  "If you'd like to help, please submit a pull request!")
        self._start_query()
        self._query.extend('class', 'announcement')
        return self.submit()

    def cdm_query(self):
        """ Initiates a cdm request. """
        raise NotImplementedError('This method is under construction.',
                                  "If you'd like to help, please submit a pull request!")
        self._start_query()
        self._query.extend('class', 'cdm')
        return self.submit()

    def organization_query(self):
        """ Initiates a organization request. """
        raise NotImplementedError('This method is under construction.',
                                  "If you'd like to help, please submit a pull request!")
        self._start_query()
        self._query.extend('class', 'organization')
        return self.submit()

    @property
    def base(self):
        return type(self)._base

    @property
    def login_url(self):
        return type(self)._login_url

    @property
    def logout_url(self):
        return type(self)._logout_url

    @property
    def null(self):
        return type(self)._null
