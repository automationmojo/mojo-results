"""
.. module:: tasknode
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the :class:`ResultNode` object used to serve as a
               tree leaf task node.

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


from typing import Any, List, Optional, Protocol

import collections
import os

from dataclasses import asdict as dataclass_as_dict

from mojo.errors.exceptions import (
    TaskingGroupAssertionError,
    TaskingGroupCancelled,
    TaskingGroupRuntimeError
)
from mojo.errors.xtraceback import (
    format_traceback_detail
)


from mojo.xmods.xdatetime import format_datetime_with_fractional
from mojo.xmods.xformatting import indent_lines_list

from mojo.results.model.resultcode import ResultCode
from mojo.results.model.resultnode import ResultNode
from mojo.results.model.resulttype import ResultType



class TaskingResult(ResultNode):
    """
        The :class:`TaskingResult` object marks a task node that contains results from a task, test or step in a result tree.  The
        result trees only store results that contain task data not associated with the hierarchy of the results.  The result tree
        does not contain results that can be computed by analyzing the relationship of the nodes in the tree.  The nodes that are
        computed are :class:`TaskingGroup` instances and do not contain instance task data.
    """
    def __init__(self, inst_id: str, name: str, parent_inst: str, worker: str, rvalue: Optional[Any] = None, 
                 result_code: ResultCode = ResultCode.UNSET, prefix: str="tasking"):
        """
            Initializes an instance of a :class:`ResultNode` object that represent the information associated with
            a specific result in a result tree.

            :param inst_id: The unique identifier for this task node.
            :param name: The name of the result container.
            :param parent_inst: The unique identifier fo this result nodes parent.
            :param worker: The name or host of the work machine that performed the tasking.
            :param rvalue: An optional value to return for the tasking.
            :param result_code: The result code to initialize the result node to.
            :param prefix: A prefix for the tasking output folder.
        """
        super().__init__(inst_id, name, parent_inst, ResultType.TASKING, result_code=result_code)

        self._worker = worker
        self._prefix = prefix
        self._rvalue = None    
        return

    @property
    def prefix(self):
        """
            The prefix that will be used for the tasking output folder.
        """
        return self._prefix

    @property
    def rvalue(self):
        """
            A value returned by the remote tasking.
        """
        return self._rvalue

    @property
    def worker(self):
        """
            The worker that will be used to execute the tasking.
        """
        return self._worker

    def add_return_value(self, rvalue: Any):
        """
            Add a result to this tasking result.
        """
        self._rvalue = rvalue
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
            ("prefix", self._prefix),
            ("worker", self._worker),
            ("start", start_datetime),
            ("stop", stop_datetime)
        ])

        if hasattr(self._rvalue, "as_dict"):
            rninfo["rvalue"] = self._rvalue.as_dict()
        else:
            rninfo["rvalue"] = self._rvalue

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


class TaskingResultFormatter(Protocol):
    
    def __call__(self, result: TaskingResult) -> List[str]: ...


def default_tasking_result_formatter(result: TaskingResult) -> List[str]:

    start_datetime = format_datetime_with_fractional(result.start)

    stop_datetime = ""
    if result.stop is not None:
        stop_datetime = format_datetime_with_fractional(result.stop)

    task_lines = [
        f"Task - {result.name} ({result.worker})",
        f"instance: {result.inst_id}",
        f"parent: {result.parent_inst}",
        f"rtype: {result.result_type.name}",
        f"result: {result.result_code.name}",
        f"start: {start_datetime}",
        f"stop: {stop_datetime}",
        f"result: {result.result}"
        f"ERRORS:"
    ]

    error_lines = []
    for item in result.errors:
        error_lines.extend(format_traceback_detail(item))
        error_lines.append("")

    error_lines = indent_lines_list(error_lines, level=1)

    task_lines.extend(error_lines)

    task_lines.append("FAILURES:")

    failure_lines = []
    for item in result.failures:
        failure_lines.extend(format_traceback_detail(item))
        failure_lines.append("")

    failure_lines = indent_lines_list(failure_lines, level=1)

    task_lines.extend(failure_lines)

    return task_lines


def verify_tasking_results(results: List[TaskingResult], context_message: str, group_name: Optional[str] = None,
                           result_formatter: TaskingResultFormatter = default_tasking_result_formatter):

    unknown_taskings = []
    cancelled_taskings = []
    errored_taskings = []
    failed_taskings = []
    passed_taskings = []

    res: TaskingResult

    for res in results:
        if res.result_code == ResultCode.PASSED:
            if len(res.errors) > 0 or len(res.failures) > 0:
                raise RuntimeError("We should never have an exception and a result code of 0.")
            
            passed_taskings.append(res)
        elif res.result_code == ResultCode.ERRORED:
            errored_taskings.append(res)
        elif res.result_code == ResultCode.FAILED:
            failed_taskings.append(res)
        elif res.result_code == ResultCode.CANCELLED:
            cancelled_taskings.append(res)
        else:
            unknown_taskings.append(res)

    if len(unknown_taskings) > 0:
        # We had taskings results of an unknown type so this condition needs to have
        # a runtime error as it should not happen
        err_msg = f"Tasking group='{group_name}' had unknown results."
        raise TaskingGroupRuntimeError(err_msg)

    elif len(cancelled_taskings) > 0:
        # All of the tasking result states were of known type, but we had some cancelled
        # taskings, so raise the cancelled error.
        err_msg = f"Tasking group='{group_name}' had cancelled tasks."
        raise TaskingGroupCancelled(err_msg)

    elif len(errored_taskings) > 0:
        # If we had any error tasks, we need to raise a non AssertionError based
        # exception
        err_msg = f"Tasking group='{group_name}' encountered Non asserted errors."
        raise TaskingGroupRuntimeError(err_msg)

    elif len(failed_taskings) > 0:
        err_msg_lines = [
            context_message,
            "RESULTS:"
        ]
        
        for res in results:
            fmt_res_lines = result_formatter(res)
            fmt_res_lines = indent_lines_list(fmt_res_lines, 1)
            err_msg_lines.extend(fmt_res_lines)
            err_msg_lines.append("")

        err_msg = os.linesep.join(err_msg_lines)

        raise TaskingGroupAssertionError(err_msg)

    return