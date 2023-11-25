"""
.. module:: resultnode
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the :class:`ResultNode` object used to serve as a
               tree leaf result node.

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


from typing import Any, Dict, List

import collections

from dataclasses import asdict as dataclass_as_dict

from mojo.results.model.resultcode import ResultCode
from mojo.results.model.resultnode import ResultNode
from mojo.results.model.resulttype import ResultType

from mojo.xmods.xdatetime import format_datetime_with_fractional

class TestResult(ResultNode):
    """
        The :class:`TestResult` object marks a result node that contains results from a task, test or step in a result tree.  The
        result trees only store results that contain result data not associated with the hierarchy of the results.  The result tree
        does not contain results that can be computed by analyzing the relationship of the nodes in the tree.  The nodes that are
        computed are :class:`ResultContainer` instances and do not contain instance result data.
    """
    def __init__(self, inst_id: str, name: str, parent_inst: str, monikers: List[str], pivots: Dict[str, Any], result_code: ResultCode = ResultCode.UNSET):
        """
            Initializes an instance of a :class:`ResultNode` object that represent the information associated with
            a specific result in a result tree.

            :param inst_id: The unique identifier to link this result container with its children.
            :param name: The name of the result container.
            :param parent_inst: The unique identifier fo this result nodes parent.
            :param monikers: The names of parameters used to extend the result name.
            :param pivots: A tuple of data pivots used for result comparisons.
            :param result_code: The result code to initialize the result node to.
        """
        super().__init__(inst_id, name, parent_inst, ResultType.TEST, result_code=result_code)

        self._monikers = monikers
        self._pivots = pivots
        self._reason = None
        self._bug = None
        return


    @property
    def monikers(self):
        """
            A list of monikers for this test.
        """
        return self._monikers

    @property
    def pivots(self):
        """
            The name of the result pivots.
        """
        return self._pivots

    def mark_skip(self, reason: str, bug: str):
        """
            Marks this result with a :class:`ResultCode` of ResultCode.SKIPPED

            :param reason: The reason the task or test this result is associated with was skipped.
        """
        self._reason = reason
        self._bug = bug
        self._result_code = ResultCode.SKIPPED
        return

    def as_dict(self, is_preview: bool = False) -> collections.OrderedDict:
        """
            Converts the result node instance to an :class:`collections.OrderedDict` object.
        """

        start_datetime = format_datetime_with_fractional(self._start)

        stop_datetime = ""
        if self._stop is not None:
            stop_datetime = format_datetime_with_fractional(self._stop)

        rninfo = collections.OrderedDict([
            ("name", self._name),
            ("monikers", self._monikers),
            ("pivots", self._pivots),
            ("instance", self._inst_id),
            ("parent", self._parent_inst),
            ("rtype", self._result_type.name),
            ("result", self._result_code.name),
            ("start", start_datetime),
            ("stop", stop_datetime)
        ])

        if not is_preview:

            errors = [dataclass_as_dict(e) for e in self._errors]
            failures = [dataclass_as_dict(f) for f in self._failures]

            detail_items = [
                ("errors", errors),
                ("failures", failures),
                ("warnings", self._warnings)
            ]

            if self._reason is not None:
                detail_items.append(("reason", self._reason))
            
            if self._bug is not None:
                detail_items.append(("bug", self._bug))
            

            detail = collections.OrderedDict(detail_items)

            if self._docstr is not None:
                detail["documentation"] =  self._docstr

            rninfo["detail"] = detail

        return rninfo

