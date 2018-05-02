SpaceTrackTool
==============
.. highlight:: python

|travis| |coveralls|

.. |travis| image:: https://travis-ci.org/Engineero/spacetracktool.svg?branch=develop
   :target: https://travis-ci.org/Engineero/spacetracktool
.. |coveralls| image:: https://coveralls.io/repos/github/Engineero/spacetracktool/badge.svg?branch=master
   :target: https://coveralls.io/github/Engineero/spacetracktool?branch=master


A Python API for making queries to space-track.org_. To install::

    $ pip install spacetracktool

To use, first get a username and password for space-track.org_, then create a
query of the desired class. For example, to create a TLE query::

    >> from spacetracktool import spacetracktool as st
    >> query = st.SpaceTrackClient('username', 'password')
    >> query.tle_query(norad_cat_id=12345)  # look for a specific satellite ID
    >> result = query.submit()  # submit to space-track.org and return the result

To create a slightly more complicated query, using ranges for some arguments::

    >> from spacetracktool import spacetracktool as st
    >> from spacetracktool import operations as ops
    >> query = st.SpaceTrackClient('username', 'password')
    >> date_range = ops.make_range_string('2018-01-01', '2018-01-31')
    >> query.tle_query(epoch=date_range)
    >> result = query.submit()

The official documents for the `space-track.org API can be found here`__.

__ https://www.space-track.org/documentation

.. _space-track.org: https://www.space-track.org/auth/login
