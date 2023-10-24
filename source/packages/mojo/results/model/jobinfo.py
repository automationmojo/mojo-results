"""
.. module:: jobinfo
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the :class:`JobInfo` dataclass used to contain and pass
               job information

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

from typing import Optional

from dataclasses import dataclass


@dataclass
class JobInfo:

    id: str # identifier for a job from the runner perspective
    name: str # name of the job.
    type: str # job type.
    owner: Optional[str] = None # Optional owner of the job.
    label: Optional[str] = None # Optional label associated with the job.
    initiator: Optional[str] = None # Optional name of the initiator of the job.
