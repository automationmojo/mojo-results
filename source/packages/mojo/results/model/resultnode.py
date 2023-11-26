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


from typing import List

import collections
import json

from datetime import datetime

from dataclasses import asdict as dataclass_as_dict

from mojo.errors.xtraceback import TracebackDetail
from mojo.results.model.resultcode import ResultCode
from mojo.results.model.resulttype import ResultType

from mojo.xmods.xdatetime import format_datetime_with_fractional

class ResultNode:
    """
        The :class:`ResultNode` object marks a result node that contains results from a task, test or step in a result tree.  The
        result trees only store results that contain result data not associated with the hierarchy of the results.  The result tree
        does not contain results that can be computed by analyzing the relationship of the nodes in the tree.  The nodes that are
        computed are :class:`ResultContainer` instances and do not contain instance result data.
    """
    def __init__(self, inst_id: str, name: str, parent_inst: str, result_type: ResultType, result_code: ResultCode = ResultCode.UNSET):
        """
            Initializes an instance of a :class:`ResultNode` object that represent the information associated with
            a specific result in a result tree.

            :param inst_id: The unique identifier to link this result container with its children.
            :param name: The name of the result container.
            :param parent_inst: The unique identifier fo this result nodes parent.
            :param result_type: The type :class:`ResultType` type code of result container.
            :param result_code: The result code to initialize the result node to.
        """
        super().__init__()

        self._inst_id = inst_id
        self._name = name
        self._parent_inst = parent_inst
        self._result_type = result_type
        self._result_code = result_code

        self._start = datetime.now()
        self._stop = None
        
        self._errors = []
        self._failures = []
        self._warnings = []
        
        self._docstr = None
        return

    @property
    def docstr(self):
        """
            Returns the documentation string associated with the tasking.
        """
        return self._docstr

    @property
    def errors(self) -> List[str]:
        """
            Returns the list of errors assocated with this result
        """
        return self._errors
    
    @property
    def failures(self) -> List[str]:
        """
            Returns the list of failures assocated with this result
        """
        return self._failures

    @property
    def inst_id(self) -> str:
        """
            The unique identifier to link this result container with its children.
        """
        return self._inst_id

    @property
    def name(self) -> str:
        """
            The name of the result item.
        """
        return self._name

    @property
    def parent_inst(self) -> str:
        """
            The unique identifier fo this result nodes parent.
        """
        return self._parent_inst

    @property
    def result_code(self) -> ResultCode:
        """
            The type :class:`ResultType` type code of result container.
        """
        return self._result_code

    @property
    def result_type(self) -> ResultType:
        """
            The :class:`ResultType` code associated with this result node.
        """
        return self._result_type
    
    @property
    def start(self) -> datetime:
        return self._start
    
    @property
    def stop(self) -> datetime:
        return self._stop

    @property
    def warnings(self) -> List[str]:
        """
            Returns the list of warnings assocated with this result
        """
        return self._warnings

    def add_error(self, trace_detail: TracebackDetail):
        """
            Adds error trace lines for a single error to this result node.
        """
        self._errors.append(trace_detail)
        return

    def add_failure(self, trace_detail: TracebackDetail):
        """
            Adds failure trace lines for a single failure to this result node.
        """
        self._failures.append(trace_detail)
        return

    def add_warning(self, warn_lines: List[str]):
        """
            Adds warning trace lines for a single warning to this result node.
        """
        trim_lines = []
        for nline in warn_lines:
            nline = nline.rstrip().replace("\r\n", "\n")
            if nline.find("\n") > -1:
                split_lines = nline.split("\n")
                trim_lines.extend(split_lines)
            else:
                trim_lines.append(nline)
        self._warnings.append(trim_lines)
        return

    def finalize(self):
        """
            Finalizes the :class:`ResultCode` code for this result node based on whether
            there were any errors or failures added to the node.
        """
        self._stop = datetime.now()

        if len(self._failures) > 0:
            self._result_code = ResultCode.FAILED
        elif len(self._errors) > 0:
            self._result_code = ResultCode.ERRORED
        elif self._result_code == ResultCode.UNSET or self._result_code == ResultCode.PASSED:
            self._result_code = ResultCode.PASSED
        else:
            self._result_code = ResultCode.UNKOWN

        return

    def mark_passed(self):
        """
            Marks this result with a :class:`ResultCode` of ResultCode.PASSED
        """
        self._result_code = ResultCode.PASSED
        return

    def set_documentation(self, docstr):
        """
            Sets the documentation string associated with this result node.
        """
        self._docstr = docstr
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

            detail = collections.OrderedDict(detail_items)

            if self._docstr is not None:
                detail["documentation"] =  self._docstr

            rninfo["detail"] = detail

        return rninfo

    def to_json(self, is_preview: bool = False) -> str:
        """
            Converts the result node instance to JSON format.
        """
        rninfo = self.as_dict(is_preview=is_preview)

        rnstr = json.dumps(rninfo, indent=4)

        return rnstr
