SpaceTrackTool
==============

Master branch
------------------

|travis_m| |coveralls_m|

.. |travis_m| image:: https://travis-ci.org/Engineero/spacetracktool.svg?branch=master
   :target: https://travis-ci.org/Engineero/spacetracktool
.. |coveralls_m| image:: https://coveralls.io/repos/github/Engineero/spacetracktool/badge.svg?branch=master
   :target: https://coveralls.io/github/Engineero/spacetracktool?branch=master

Development branch
------------------

|travis_d| |coveralls_d|

.. |travis_d| image:: https://travis-ci.org/Engineero/spacetracktool.svg?branch=develop
   :target: https://travis-ci.org/Engineero/spacetracktool
.. |coveralls_d| image:: https://coveralls.io/repos/github/Engineero/spacetracktool/badge.svg?branch=develop
   :target: https://coveralls.io/github/Engineero/spacetracktool?branch=develop


A Python API for making queries to space-track.org_. To install::

    pip install spacetracktool

To use, first get a username and password for space-track.org_, then create a
query of the desired class. For example, to create a TLE query::

.. code-block:: python
    import spacetracktool as st
    query = st.SpaceTrackClient('username', 'password')
    result = query.tle_query(norad_cat_id=12345)  # look for a specific satellite ID

To create a slightly more complicated query, using ranges for some arguments::

.. code-block:: python
    import spacetracktool as st
    from spacetracktool import operations as ops
    query = st.SpaceTrackClient('username', 'password')
    date_range = ops.make_range_string('2018-01-01', '2018-01-31')
    result = query.tle_query(epoch=date_range)  # generates and submits query

The official documents for the `space-track.org API can be found here`__.

__ https://www.space-track.org/documentation

.. _space-track.org: https://www.space-track.org/auth/login
