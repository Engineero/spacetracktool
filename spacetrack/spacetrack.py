import requests

class _SpaceTrackBase():
    """ Provides an API for making POST requests to space-track.org
    
    Properties:
        base: the base URL used for generating queries.
        login_url: the URL used to log in to space-track.org.
        logout_url: the URL used to send a logout request to space-track.org.
    """
    _base = 'https://space-track.org/'  # base URL for requests
    _login_url = 'https://www.space-track.org/ajaxauth/login'  # login URL
    _logout_url = 'https://www.space-track.org/ajaxauth/logout'
    _null = 'null-val'  # string used by space-track for null values

    def __init__(self, username: str, password: str, fmt: str=None):
        """ Initializes the API.
        
        This API class can be used to build and submit requests to
        space-track.org.
        
        Args:
            username: your space-track.org username.
            password: the associated password.
        
        Kwargs:
            fmt: string specifying format for returned message. Can be one of
                'xml', 'json', 'html', 'csv', 'tle', '3le', 'kvn', or None.
                None is the same as 'json'. Default is None.
        
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

    def _make_range_string(self, start: str=None, end: str=None,
                           equal: bool=False) -> str:
        """ Generates a string based on input range and mode.
        
        If `equal` is True, returns `start` or `end` (if `start` is None). If
        `equal` is False, retruns `'>[start]'` if only `start` is given,
        returns `'<[end]'` if only `end` is given, and returns
        `'[start]--[end]'` if both are given. Note that no range checking is
        performed on the input strings to ensure the result is a valid range.
        
        Kwargs:
            start: the starting (lowest) value of the string. Default is None.
            end: the end (highest) value of the string. Default is None.
            equal: if True, returns `start` if defined, otherwise `end`.  If
                False, returns a range based on values of `start` and `end`.
                Default is False.
        
        Returns:
            Resulting range string.
        
        Raises:
            ValueError: if neither `start` nor `end` is specified and `equal`
                is `True`.
            ValueError: if neither `start` nor `end` (or both) is specified and
                `equal` is `False`.
        """
        result = None
        if equal:
            if start is not None:
                result = start
            elif end is not None:
                result = end
            else:
                raise ValueError("Either 'start' or 'end' must be specified \
                                  if 'equal' is True.")
        else:
            if start is not None and end is not None:
                result = start + '--' + end
            elif start is not None and end is None:
                result = '>' + start
            elif start is None and end is not None:
                result = '<' + end
            else:
                raise ValueError("Either 'start' or 'end' or both must be \
                                  specified if 'equal' is False.")
        return result

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



class _SatelliteIdMixin():
    """ Mixin class for specifying methods associate with satellite IDs.

    This class has the methods used for querying according to NORAD catalog ID,
    satellite name, etc.
    """
    def norad_cat_id(self, id_number: int):
        """ Specifies the NORAD_CAT_ID field in the query.
        
        Use this to find a specific satellite in the catalog.
        
        Args:
            id_number: the catalog ID number of the satellite.
        """
        self._query.extend('NORAD_CAT_ID', str(id_number))

    def object_name(self, obj_name: str):
        self._query.extend('OBJECT_NAME', str(obj_name))

    def object_type(self, obj_type: str):
        self._query.extend('OBJECT_TYPE', str(obj_type))

    def object_id(self, obj_id: str):
        self._query.extend('OBJECT_ID', str(obj_id))

    def object_number(self, obj_num: int):
        self._query.extend('OBJECT_ID', str(obj_num))


class _OrbitMixin():
    """ Specifies most common methods for querying orbit information. """
    def period(self, low: float=None, high: float=None, equal: bool=False):
        self._query.extend('PERIOD',
                           self._make_range_string(str(low), str(high), equal))

    def apogee(self, low: float=None, high: float=None, equal: bool=False):
        self._query.extend('APOGEE',
                           self._make_range_string(str(low), str(high), equal))

    def perigee(self, low: float=None, high: float=None, equal: bool=False):
        self._query.extend('PERIGEE',
                           self._make_range_string(str(low), str(high), equal))

    def inclination(self, low: float=None, high: float=None,
                    equal: bool=False):
        self._query.extend('INCLINATION',
                           self._make_range_string(str(low), str(high), equal))


class _ElsetMixin(_OrbitMixin):
    """ Specifies methods used for ELSET-related queries.

    Specifies those methods related to the element sets, e.g. the inclination,
    right-ascension, mean motion, etc.
    """
    def epoch(self, start: str=None, end: str=None, equal: bool=False):
        """ Specifies a date range for the EPOCH field in the query.
        
        If only a start date is specified and 'equal' is set to 'False', the
        query will look for epochs on or after the start date. If both a start
        and end date are specified, the query will look for the range between
        those dates. If only an end date is specified and 'equal' is set to
        'False', the query will look for epochs on or before the end date.
        
        'equal' can be set to 'True', in which case it will look for epochs
        exactly on the start date (if specified) or end date if no start date
        is specified.
        
        All dates are datetime-formatted strings of the form:
        
            YYYY-MM-DD HH:mm:ss

        or

            YYYY-MM-DD
        
        Kwargs:
            start: start date as a datetime-formatted string.
            end: end date as a datetime-formatted string.
            equal: if False, looks for dates greater than the start date if
                only a start date is specified, less than the end date if only
                an end date is specified, and between the start and end dates
                if both are specified.
        
        Raises:
            ValueError: if neither `start` nor `end` is specified and `equal`
                is `True`.
            ValueError: if neither `start` nor `end` (or both) is specified and
                `equal` is `False`.
        """
        self._query.extend('EPOCH', self._make_range_string(start, end, equal))

    def epoch_us(self, low: int=None, high: int=None, equal: bool=False):
        self._query.extend('EPOCH_MICROSECONDS',
                           self._make_range_string(low, high, equal))

    def mean_motion(self, low: float=None, high: float=None, equal: bool=False):
        self._query.extend('MEAN_MOTION',
                           self._make_range_string(str(low), str(high), equal))

    def eccentricity(self, low: float=None, high: float=None,
                     equal: bool=False):
        self._query.extend('ECCENTRICITY',
                           self._make_range_string(str(low), str(high), equal))

    def ra_of_asc_node(self, low: float=None, high: float=None,
                       equal: bool=False):
        self._query.extend('RA_OF_ASC_NODE',
                           self._make_range_string(str(low), str(high), equal))

    def arg_of_pericenter(self, low: float=None, high: float=None,
                          equal: bool=False):
        self._query.extend('ARG_OF_PERICENTER',
                           self._make_range_string(str(low), str(high), equal))

    def mean_anomaly(self, low: float=None, high: float=None,
                     equal: bool=False):
        self._query.extend('MEAN_ANOMALY',
                           self._make_range_string(str(low), str(high), equal))

    def element_set_no(self, number: int):
        self._query.extend('ELEMENT_SET_NO', str(number))

    def rev_at_epoch(self, low: float=None, high: float=None,
                     equal: bool=False):
        self._query.extend('MEAN_ANOMALY',
                           self._make_range_string(str(low), str(high), equal))

    def bstar(self, low: float=None, high: float=None, equal: bool=False):
        self._query.extend('BSTAR',
                           self._make_range_string(str(low), str(high), equal))

    def mean_motion_dot(self, low: float=None, high: float=None, equal:
                        bool=False):
        self._query.extend('MEAN_MOTION_DOT',
                           self._make_range_string(str(low), str(high), equal))

    def mean_motion_ddot(self, low: float=None, high: float=None,
                         equal: bool=False):
        self._query.extend('MEAN_MOTION_DDOT',
                           self._make_range_string(str(low), str(high), equal))

    def semimajor_axis(self, low: float=None, high: float=None,
                       equal: bool=False):
        self._query.extend('SEMIMAJOR_AXIS',
                           self._make_range_string(str(low), str(high), equal))


class TleQuery(_SpaceTrackBase, _SatelliteIdMixin, _ElsetMixin):
    """ TLE request from space-track.org. """
    def __init__(self, *args, **kwargs):
        """ Initiates a TLE request.
        
        Args:
            username: your space-track.org username.
            password: the associated password.
        
        Kwargs:
            fmt: string specifying format for returned message. Can be one of
                'xml', 'json', 'html', 'csv', 'tle', '3le', 'kvn', or None. None
                is the same as 'json'. Default is None.
        """
        self._start_query()
        self._query.extend('class', 'tle')
        super().__init__(*args, **kwargs)




class TleLatestQuery(_SpaceTrackBase, _ElsetMixin):
    """ TLE Latest request from space-track.org. """
    def __init__(self, *args, **kwargs):
        """ Initiates a tle_latest request. """
        self._start_query()
        self._query.extend('class', 'tle_latest')
        super().__init__(*args, **kwargs)


class BoxScoreQuery(_SpaceTrackBase):
    def __init__(self, *args, **kwargs):
        """ Initiates a boxscore request. """
        raise NotImplementedError('This class is under construction.') 
        self._start_query()
        self._query.extend('class', 'boxscore')
        super().__init__(*args, **kwargs)


class SatCatQuery(_SpaceTrackBase, _OrbitMixin):
    def __init__(self, *args, **kwargs):
        """ Initiates a satcat request. """
        self._start_query()
        self._query.extend('class', 'satcat')
        super().__init__(*args, **kwargs)

    def country(self, country: str):
        self._query.extend('COUNTRY', country)

    def launch(self, low: str=None, high: str=None, equal: bool=False):
        """ Sets the launch date range for the search. """
        self._query.extend('LAUNCH',
                           self._make_range_string(str(low), str(high), equal))

    def site(self, site: str):
        self._query.extend('SITE', site)


class LaunchSiteQuery(_SpaceTrackBase):
    def __init__(self, *args, **kwargs):
        """ Initiates a launch_site request. """
        raise NotImplementedError('This class is under construction.') 
        self._start_query()
        self._query.extend('class', 'launch_site')
        super().__init__(*args, **kwargs)


class SatCatChangeQuery(_SpaceTrackBase):
    def __init__(self, *args, **kwargs):
        """ Initiates a satcat_change request. """
        raise NotImplementedError('This class is under construction.') 
        self._start_query()
        self._query.extend('class', 'satcat_change')
        super().__init__(*args, **kwargs)


class SatCatDebutQuery(_SpaceTrackBase):
    def __init__(self, *args, **kwargs):
        """ Initiates a satcat_debut request. """
        raise NotImplementedError('This class is under construction.') 
        self._start_query()
        self._query.extend('class', 'satcat_debut')
        super().__init__(*args, **kwargs)


class DecayQuery(_SpaceTrackBase):
    def __init__(self, *args, **kwargs):
        """ Initiates a decay request. """
        raise NotImplementedError('This class is under construction.') 
        self._start_query()
        self._query.extend('class', 'decay')
        super().__init__(*args, **kwargs)


class AnnouncementQuery(_SpaceTrackBase):
    def __init__(self, *args, **kwargs):
        """ Initiates a announcement request. """
        raise NotImplementedError('This class is under construction.') 
        self._start_query()
        self._query.extend('class', 'announcement')
        super().__init__(*args, **kwargs)


class CdmQuery(_SpaceTrackBase):
    def __init__(self, *args, **kwargs):
        """ Initiates a cdm request. """
        raise NotImplementedError('This class is under construction.') 
        self._start_query()
        self._query.extend('class', 'cdm')
        super().__init__(*args, **kwargs)


class OrganizationQuery(_SpaceTrackBase):
    def __init__(self, *args, **kwargs):
        """ Initiates a organization request. """
        raise NotImplementedError('This class is under construction.') 
        self._start_query()
        self._query.extend('class', 'organization')
        super().__init__(*args, **kwargs)
