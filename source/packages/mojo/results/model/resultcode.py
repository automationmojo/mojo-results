"""
.. module:: resulttype
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the :class:`ResultType` enumeration used to mark the result code
               for a leaf/task node.

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

from enum import IntEnum

class ResultCode(IntEnum):
    """
        Enumeration that summarizes a result.
    """
    UNSET = 0
    PASSED = 1
    SKIPPED = 2
    ERRORED = 3
    FAILED = 4
    CANCELLED = 5
    UNKOWN = 6
