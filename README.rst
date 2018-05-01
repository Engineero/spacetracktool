SpaceTrackTool
==============

.. highlight:: python

A Python API for making queries to space-track.org_. To install::

    $ pip install spacetracktool

To use, first get a username and password for space-track.org_, then create a
query of the desired class. For example, to create a TLE query::

    >> import spacetracktool as st
    >> query = st.SpaceTrackClient(username, password)
    >> query.tle_query(norad_cat_id=12345)  # look for a specific satellite ID
    >> result = query.submit()  # submit to space-track.org and return the result

To create a slightly more complicated query, using ranges for some arguments::

    >> import spacetracktool as st
    >> import spacetracktool.operations as ops
    >> query = st.SpaceTrackClient(username, password)
    >> date_range = ops.make_range_string('2018-01-01', '2018-01-31')
    >> query.tle_query(epoch=date_range)
    >> result = query.submit()

The official documents for the `space-track.org API can be found here`__.

__ https://www.space-track.org/documentation#/api

.. _space-track.org: https://www.space-track.org/auth/login
