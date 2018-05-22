""" Module for making queries to space-track.org.

The main entry point of the module is the SpaceTrackClient class. To start,
create an instance of the SpaceTrackClient passing your username and password
for space-track.org. You can sign up for a free account at space-track.org. ::

    import spacetracktool as st
    client = SpaceTrackClient('username', 'password')

Any query class defined in the space-track.org API is implemented as a method
of this client, but not all classes have been tested as of yet. If you find
problems, please open an issue on the project's GitHub page or submit a pull
request.

"""
from .spacetrackclient import SpaceTrackClient
from .version import __version__
