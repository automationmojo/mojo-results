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


from dataclasses import dataclass


@dataclass
class PipelineInfo:

    id: str # identifier such as a uuid which identifies a particular venue associated with the pipeline.
    name: str # name for the venue associated pipeline.
    instance: str # identifier such as a uuid which identifies an instance of a pipeline.