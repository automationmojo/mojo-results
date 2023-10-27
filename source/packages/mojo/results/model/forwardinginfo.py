"""
.. module:: forwardinginfo
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the :class:`ForwardingInfo` dataclass used to contain and pass
               summary forwarding parameter information

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
class ForwardingInfo:

    forwarding_interval: float # The interval in seconds to use when forwarding job summary information
    forwarding_url: str # identifier such as a uuid which identifies a particular pipeline.
    forwarding_headers: Optional[dict] = None # Headers to use when forwarding progress, results or summaries.
