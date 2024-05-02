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


from typing import Optional


from dataclasses import dataclass


@dataclass
class ForwardingInfo:

    forwarding_interval: float # The interval in seconds to use when forwarding job summary information
    forwarding_url: str # identifier such as a uuid which identifies a particular pipeline.
    forwarding_headers: Optional[dict] = None # Headers to use when forwarding progress, results or summaries.
