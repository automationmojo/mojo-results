"""
.. module:: pipelineinfo
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the :class:`PipelineInfo` dataclass used to contain and pass
               pipeline information

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
class PipelineInfo:

    id: str # identifier such as a uuid which identifies a particular pipeline.
    name: str # name for the associated pipeline.
    instance: str # identifier such as a uuid which identifies an instance of a pipeline.