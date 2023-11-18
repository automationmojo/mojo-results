"""
.. module:: resulttype
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the :class:`ResultType` enumeration used to mark the type of
               a result node.

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

class ResultType(IntEnum):
    """
        Enumeration to mark the type of result.
    """
    JOB = 0
    PACKAGE = 1
    SCOPE = 2
    TASK_CONTAINER = 3
    TASK = 4
    TEST_CONTAINER = 5
    TEST = 6
    STEP_CONATINER = 7
    STEP = 8
    TASKING_GROUP = 9
    TASKING = 10
