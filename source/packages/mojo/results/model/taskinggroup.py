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


import collections

from datetime import datetime

from mojo.results.model.resulttype import ResultType
from mojo.results.model.resultcontainer import ResultContainer

from mojo.xmods.xdatetime import format_datetime_with_fractional


class TaskingGroup(ResultContainer):
    """
        The :class:`TaskingGroup` instances are group nodes that are used to link result nodes in the
        result tree.  The :class:`TaskingGroup` nodes do not contain result data but link data so the data can
        be computed on demand.
    """
    def __init__(self, inst_id: str, name: str, parent_inst: str):
        """
            Creates an instance of a result group.

            :param inst_id: The unique identifier to link this result group with its children.
            :param name: The name of the result group.
            :param parent_inst: The unique identifier fo this result nodes parent.
        """
        super().__init__(inst_id, name, ResultType.TASKING_GROUP, parent_inst=parent_inst)

        self._start = datetime.now()
        self._stop = None
        return

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

    def as_dict(self, is_preview: bool = False) -> collections.OrderedDict:
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
