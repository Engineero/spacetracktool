SpaceTrack
==========

A Python API for making queries to space-track.org_. To install::

    pip install spacetrack

To use, first get a username and password for space-track.org_, then create a
query of the desired class. For example, to create a TLE query::

.. highlight:: python

    import spacetrack as st
    tle_query = st.TleQuery(username, password)
    tle_query.norad_cat_id(12345)  # look for a specific satellite ID
    tle = tle_query.submit()  # submit to space-track.org and return the result

The official documents for the `space-track.org API can be found here`__.

__ https://www.space-track.org/documentation#/api

.. _space-track.org: https://www.space-track.org/auth/login
