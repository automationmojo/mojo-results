"""
.. module:: buildinfo
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the :class:`BuildInfo` dataclass used to contain and pass
               build information

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"



from dataclasses import dataclass


@dataclass
class BuildInfo:

    branch: str # name of a code 'branch' to associate with the results.
    build: str # name of a product 'build' to associate with the results
    flavor: str # label that indicates the flavor of build the automation is running against.
    release: str # name of a release to associate a automation run with.
    url: str # build url
