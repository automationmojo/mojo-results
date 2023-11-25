"""
.. module:: resultcontainer
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the :class:`ResultContainer` object used to serve as a
               tree node container for child results.

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

from mojo.results.model.resulttype import ResultType

class ResultContainer:
    """
        The :class:`ResultContainer` instances are container nodes that are used to link result nodes in the
        result tree.  The :class:`ResultContainer` nodes do not contain result data but link data so the data can
        be computed on demand.
    """
    def __init__(self, inst_id: str, name: str, result_type: ResultType, parent_inst: Optional[str] = None):
        """
            Creates an instance of a result container.

            :param inst_id: The unique identifier to link this result container with its children.
            :param name: The name of the result container.
            :param result_type: The type :class:`ResultType` type code of result container.
            :param parent_inst: The unique identifier fo this result nodes parent.
        """
        super().__init__()

        self._inst_id = inst_id
        self._name = name
        self._result_type = result_type
        self._parent_inst = parent_inst
        return

    @property
    def inst_id(self) -> str:
        """
            The unique identifier to link this result container with its children.
        """
        return self._inst_id

    @property
    def name(self) -> str:
        """
            The name of the result container.
        """
        return self._name

    @property
    def parent_inst(self) -> str:
        """
            The unique identifier fo this result nodes parent.
        """
        return self._parent_inst

    @property
    def result_type(self) -> ResultType:
        """
            The type :class:`ResultType` type code of result container.
        """
        return self._result_type

    def as_dict(self, is_preview: bool = False) -> collections.OrderedDict:
        """
            Converts the result container instance to an :class:`collections.OrderedDict` object.
        """
        rcinfo = collections.OrderedDict([
            ("name", self._name),
            ("instance", self._inst_id),
            ("parent", self._parent_inst),
            ("rtype", self._result_type.name)
        ])

        return rcinfo

    def to_json(self, is_preview: bool = False) -> str:
        """
            Converts the result container instance to JSON format.
        """
        rcinfo = self.as_dict(is_preview=is_preview)

        rcstr = json.dumps(rcinfo, indent=4)

        return rcstr