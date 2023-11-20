"""
.. module:: taskgroup
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the :class:`TaskingGroup` object used to serve as a
               tree node group for a group of tasks.

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

import collections
import json

from datetime import datetime

from mojo.results.model.resulttype import ResultType

from mojo.xmods.xdatetime import format_datetime_with_fractional


class TaskingGroup:
    """
        The :class:`TaskingGroup` instances are group nodes that are used to link result nodes in the
        result tree.  The :class:`TaskingGroup` nodes do not contain result data but link data so the data can
        be computed on demand.
    """
    def __init__(self, inst_id: str, name: str, parent_inst: str, result_type: ResultType):
        """
            Creates an instance of a result group.

            :param inst_id: The unique identifier to link this result group with its children.
            :param name: The name of the result group.
            :param parent_inst: The unique identifier fo this result nodes parent.
            :param result_type: The type :class:`ResultType` type code of result group.
        """
        super().__init__()

        self._inst_id = inst_id
        self._name = name
        self._parent_inst = parent_inst
        self._result_type = result_type
        self._start = datetime.now()
        self._stop = None
        return

    @property
    def parent_inst(self) -> str:
        """
            The unique identifier fo this result nodes parent.
        """
        return self._parent_inst

    @property
    def inst_id(self) -> str:
        """
            The unique identifier to link this result group with its children.
        """
        return self._inst_id

    @property
    def name(self) -> str:
        """
            The name of the result group.
        """
        return self._name

    @property
    def result_type(self) -> ResultType:
        """
            The type :class:`ResultType` type code of result group.
        """
        return self._result_type

    @property
    def start(self):
        """
            The start timestamp of the tasking group.
        """
        return self._start
    
    @property
    def stop(self):
        """
            The stop timestamp of the tasking group.
        """
        return self._stop

    def finalize(self):
        self._stop = datetime.now()
        return

    def as_dict(self) -> collections.OrderedDict:
        """
            Converts the result group instance to an :class:`collections.OrderedDict` object.
        """

        start_datetime = format_datetime_with_fractional(self._start)

        stop_datetime = ""
        if self._stop is not None:
            stop_datetime = format_datetime_with_fractional(self._stop)

        rcinfo = collections.OrderedDict([
            ("name", self._name),
            ("instance", self._inst_id),
            ("parent", self._parent_inst),
            ("rtype", self._result_type.name),
            ("start", start_datetime),
            ('stop', stop_datetime)
        ])

        return rcinfo

    def to_json(self) -> str:
        """
            Converts the result group instance to JSON format.
        """
        rcinfo = self.as_dict()

        rcstr = json.dumps(rcinfo, indent=4)

        return rcstr