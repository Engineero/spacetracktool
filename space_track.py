import requests

class _SpaceTrack():
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

    def __init__(self, username: str, password: str, fmt: str=None):
        """ Initializes the API.
        
        This API class can be used to build and submit requests to space-track.org.
        
        Args:
            username: your space-track.org username.
            password: the associated password.
        
        Kwargs:
            fmt: string specifying format for returned message. Can be one of
            'xml', 'json', 'html', 'csv', 'tle', '3le', 'kvn', or None. None
            is the same as 'json'. Default is None.
        
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
        
        If `equal` is True, returns `start` or `end` (if `start` is None).
        If `equal` is False, retruns `'>[start]'` if only `start` is given,
        returns `'<[end]'` if only `end` is given, and returns `'start--end'`
        if both are given. Note that no range checking is performed on the
        input strings to ensure the result is a valid range.
        
        Kwargs:
            start: the starting (lowest) value of the string. Default is None.
            end: the end (highest) value of the string. Default is None.
            equal: if True, returns `start` if defined, otherwise `end`.
                If False, returns a range based on values of `start` and
                `end`. Default is False.
        
        Returns:
            Resulting range string.
        
        Raises:
            ValueError: if neither `start` nor `end` is specified and `equal`
                is `True`.
            ValueError: if neither `start` nor `end` (or both) is specified
                and `equal` is `False`.
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
        
        Note that at this stage the format string has not been applied to
        the query. This string gets applied at the very end prior to
        submitting the POST request.
        """
        print('/'.join(self._query))

    def submit(self) -> requests.models.Response:
        """ Submits the generated query to space-track.org and returns the response.
        
        Returns:
            Response from space-track.org
        """
        payload = {'identity': self.username,
                   'password': self.password,
                   'query': self._compile_query()}
        self.result = requests.post(self.login_url, data=payload)
        if not self.result.ok:
            print('Error posting request! Status code {}'.format(self.result.status_code))
        self._logout()
        return self.result


class TleQuery(_SpaceTrack):
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

    def norad_cat_id(self, id_number: int):
        """ Specifies the NORAD_CAT_ID field in the query.
        
        Use this to find a specific satellite in the catalog.
        
        Args:
            id_number: the catalog ID number of the satellite.
        """
        self._query.extend('NORAD_CAT_ID', str(id_number))

    def epoch(self, start: str=None, end: str=None, equal: bool=False):
        """ Specifies a date range for the EPOCH field in the query.
        
        If only a start date is specified and 'equal' is set to 'False',
        the query will look for epochs on or after the start date. If
        both a start and end date are specified, the query will look
        for the range between those dates. If only an end date is
        specified and 'equal' is set to 'False', the query will look for
        epochs on or before the end date.
        
        'equal' can be set to 'True', in which case it will look for
        epochs exactly on the start date (if specified) or end date
        if no start date is specified.
        
        All dates are datetime-formatted strings of the form:
        
            YYYY-MM-DD HH:mm:ss

        or

            YYYY-MM-DD
        
        Kwargs:
            start: start date as a datetime-formatted string.
            end: end date as a datetime-formatted string.
            equal: if False, looks for dates greater than the start date
                if only a start date is specified, less than the end date
                if only an end date is specified, and between the start
                and end dates if both are specified.
        
        Raises:
            ValueError: if neither `start` nor `end` is specified and `equal`
                is `True`.
            ValueError: if neither `start` nor `end` (or both) is specified
                and `equal` is `False`.
        """
        self._query.extend('EPOCH', self._make_range_string(start, end, equal))


class TleLatestQuery(_SpaceTrack):
    """ TLE Latest request from space-track.org. """
    def __init__(self, *args, **kwargs):
        """ Initiates a tle_latest request. """
        raise NotImplementedError('This class is under construction.') 
        self._start_query()
        self._query.extend('class', 'tle_latest')
        super().__init__(*args, **kwargs)


class TlePublishQuery(_SpaceTrack):
    """ TLE Publish request from space-track.org. """
    def __init__(self, *args, **kwargs):
        """ Initiates a tle_publish request. """
        raise NotImplementedError('This class is under construction.') 
        self._start_query()
        self._query.extend('class', 'tle_publish')
        super().__init__(*args, **kwargs)


class BoxScoreQuery(_SpaceTrack):
    def __init__(self, *args, **kwargs):
        """ Initiates a boxscore request. """
        raise NotImplementedError('This class is under construction.') 
        self._start_query()
        self._query.extend('class', 'boxscore')
        super().__init__(*args, **kwargs)


class SatCatQuery(_SpaceTrack):
    def __init__(self, *args, **kwargs):
        """ Initiates a satcat request. """
        raise NotImplementedError('This class is under construction.') 
        self._start_query()
        self._query.extend('class', 'satcat')
        super().__init__(*args, **kwargs)


class LaunchSiteQuery(_SpaceTrack):
    def __init__(self, *args, **kwargs):
        """ Initiates a launch_site request. """
        raise NotImplementedError('This class is under construction.') 
        self._start_query()
        self._query.extend('class', 'launch_site')
        super().__init__(*args, **kwargs)


class SatCatChangeQuery(_SpaceTrack):
    def __init__(self, *args, **kwargs):
        """ Initiates a satcat_change request. """
        raise NotImplementedError('This class is under construction.') 
        self._start_query()
        self._query.extend('class', 'satcat_change')
        super().__init__(*args, **kwargs)


class SatCatDebutQuery(_SpaceTrack):
    def __init__(self, *args, **kwargs):
        """ Initiates a satcat_debut request. """
        raise NotImplementedError('This class is under construction.') 
        self._start_query()
        self._query.extend('class', 'satcat_debut')
        super().__init__(*args, **kwargs)


class DecayQuery(_SpaceTrack):
    def __init__(self, *args, **kwargs):
        """ Initiates a decay request. """
        raise NotImplementedError('This class is under construction.') 
        self._start_query()
        self._query.extend('class', 'decay')
        super().__init__(*args, **kwargs)


class AnnouncementQuery(_SpaceTrack):
    def __init__(self, *args, **kwargs):
        """ Initiates a announcement request. """
        raise NotImplementedError('This class is under construction.') 
        self._start_query()
        self._query.extend('class', 'announcement')
        super().__init__(*args, **kwargs)


class CdmQuery(_SpaceTrack):
    def __init__(self, *args, **kwargs):
        """ Initiates a cdm request. """
        raise NotImplementedError('This class is under construction.') 
        self._start_query()
        self._query.extend('class', 'cdm')
        super().__init__(*args, **kwargs)


class OrganizationQuery(_SpaceTrack):
    def __init__(self, *args, **kwargs):
        """ Initiates a organization request. """
        raise NotImplementedError('This class is under construction.') 
        self._start_query()
        self._query.extend('class', 'organization')
        super().__init__(*args, **kwargs)
