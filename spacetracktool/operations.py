""" Operations for use with the SpaceTrackClient.
"""

def make_range_string(start: str=None, end: str=None, equal: bool=False) -> str:
        """ Generates a string based on input range and mode.
        
        If `equal` is True, returns `start` or `end` (if `start` is None). If
        `equal` is False, retruns `'>[start]'` if only `start` is given,
        returns `'<[end]'` if only `end` is given, and returns
        `'[start]--[end]'` if both are given. Note that no range checking is
        performed on the input strings to ensure the result is a valid range.
        
        Kwargs:

            start: str or value coercable to str.
                The starting (lowest) value of the string. Default is None.

            end: str or value coercable to str.
                The end (highest) value of the string. Default is None.

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

            ValueError: if start or end cannot be coerced to string.

        """
        if start is not None:
            if not isinstance(start, str):
                try:
                    start = str(start)
                except Exception as e:
                    print(e)
                    raise ValueError('start must be a string or coercable to',
                                     'string!')
        if end is not None:
            if not isinstance(end, str):
                try:
                    end = str(end)
                except Exception as e:
                    print(e)
                    raise ValueError('end must be a string or coercable to',
                                     'string!')
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

