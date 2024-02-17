"""
.. module:: resultrecorder
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the :class:`ResultRecorder` object.

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


from typing import List, Optional

from types import TracebackType

import collections
import copy
import os
import shutil
import threading

from datetime import datetime

from mojo.errors.exceptions import NotOverloadedError

from mojo.xmods.jsos import CHAR_RECORD_SEPERATOR

from mojo.results.model.buildinfo import BuildInfo
from mojo.results.model.jobinfo import JobInfo
from mojo.results.model.pipelineinfo import PipelineInfo
from mojo.results.model.renderinfo import RenderInfo

from mojo.results.model.resultcode import ResultCode
from mojo.results.model.resultnode import ResultNode
from mojo.results.model.resulttype import ResultType

from mojo.results.utilities import (
    catalog_tree,
    DEFAULT_DO_NOT_CATALOG_DIRS,
    DEFAULT_DO_NOT_DESCEND_DIRS
)

from mojo.results.model.progresscode import ProgressCode
from mojo.results.model.progressinfo import ProgressInfo
from mojo.results.model.forwardinginfo import ForwardingInfo

class ResultRecorder:
    """
        The :class:`ResultRecorder` object is the base class object that establishes the API patterns
        for recorders of different formats to use when implementing a test result recorder.
    """
    def __init__(self, *, runid: str, start: datetime, render_info: RenderInfo,
                 apod: Optional[str] = None, build_info: Optional[BuildInfo] = None,
                 pipeline_info: Optional[PipelineInfo] = None, job_info: Optional[JobInfo] = None,
                 forwarding_info: Optional[ForwardingInfo] = None):
        """
            Initializes an instance of a ResultRecorder with the information about a test run.

            :param runid: The uuid string that identifies a set of test results.
            :param start: The date and time of the start of the test run.
            :param render_info: Automation results rendering info
            :param apod: Optional name of an automation pod that the automation run is running on.
            :param build_info: Optional build information to associate with an automation run.
            :param pipeline_info: Optional pipeline information to associate with an automation run.
            :param job_info: Optional job information to associate with an automation run.
            
        """

        self._runid = runid
        self._start = start
        self._apod = apod

        self._render_info = render_info
        self._build_info = build_info
        self._pipeline_info = pipeline_info
        self._job_info = job_info
        self._forwarding_info = forwarding_info

        self._output_dir = os.path.dirname(self._render_info.summary_filename)

        self._rout = None

        self._running_tasks = {}

        self._error_count = 0
        self._failure_count = 0
        self._pass_count = 0
        self._skip_count = 0
        self._unknown_count = 0

        self._total_count = 0

        self._finalized = False

        build_info = collections.OrderedDict((
            ("release", self._build_info.release),
            ("branch", self._build_info.branch),
            ("build", self._build_info.build),
            ("flavor", self._build_info.flavor),
            ("url", self._build_info.url)
        ))

        pipeline_info = collections.OrderedDict((
            ("id", self._pipeline_info.id),
            ("name", self._pipeline_info.name),
            ("instance", self._pipeline_info.instance)
        ))

        job_info = collections.OrderedDict((
            ("id", self._job_info.id),
            ("initiator", self._job_info.initiator),
            ("label", self._job_info.label),
            ("name", self._job_info.name),
            ("owner", self._job_info.owner),
            ("type", self._job_info.type)
        ))

        self._summary = collections.OrderedDict((
            ("title", self._render_info.title),
            ("runid", self._runid),
            ("build", build_info),
            ("pipeline", pipeline_info),
            ("job", job_info),
            ("start", self._start),
            ("stop", None),
            ("result", "RUNNING"),
            ("apod", self._apod),
            ("detail", None),
            ("running", self._running_tasks)
        ))

        self._lock = threading.Lock()
        self._next_forward_at = None

        return

    def __enter__(self):
        """
            Starts up the recording process of test results.
        """
        self.initialize_report()

        self.update_summary()
        
        self._rout = open(self._render_info.result_filename, 'w')
        return self

    def __exit__(self, ex_type: type, ex_inst: Exception, ex_tb: TracebackType) -> bool:
        """
            Starts up the recording process of test results.

            :param ex_type: The type associated with the exception being raised.
            :param ex_inst: The exception instance of the exception being raised.
            :param ex_tb: The traceback associated with the exception being raised.

            :returns: Returns true if an exception was handled and should be suppressed.
        """
        if not self._finalized:
            self.finalize()
        return

    @property
    def summary(self):
        """
            Get the result summary.
        """
        rtnval = None

        self._lock.acquire()
        try:
            rtnval = copy.deepcopy(self._summary)
        finally:
            self._lock.release()

        return rtnval

    def catalog_output_directory(self):
        """
            A method that can be called in order to trigger catalog generation for the
            results output directory.
        """
        catalog_tree(self._output_dir, dont_catalog_dirs=DEFAULT_DO_NOT_CATALOG_DIRS,
                     dont_descend_dirs=DEFAULT_DO_NOT_DESCEND_DIRS)
        return

    def finalize(self):
        """
            Finalizes the test results counters and status of the test run.
        """

        self._lock.acquire()
        try:

            self._finalized = True

            self._stop = datetime.now()
            self._summary["stop"] = str(self._stop)

            self._summary["detail"] = {
                "errors": self._error_count,
                "failed": self._failure_count,
                "skipped": self._skip_count,
                "passed": self._pass_count,
                "total": self._total_count
            }

            if self._error_count > 0 or self._failure_count > 0:
                self._summary["result"] = "FAILED"
            else:
                self._summary["result"] = "PASSED"

            self._rout.close()

            self.update_summary()

        finally:
            self._lock.release()

        return
    
    def format_lines(self):
        lines = [
            " ============== Test Summary ============== ",
        ]

        if self._render_info.title:
            lines.append("   Title: {}".format(self._render_info.title))

        if self._build_info is not None:
            if self._build_info.release:
                lines.append("  Release: {}".format(self._build_info.release))
            if self._build_info.branch:
                lines.append("  Branch: {}".format(self._build_info.branch))
            if self._build_info.build:
                lines.append("   Build: {}".format(self._build_info.build))
            if self._build_info.flavor:
                lines.append("  Flavor: {}".format(self._build_info.flavor))

        if self._job_info is not None:
            if self._job_info.owner:
                lines.append("   Owner: {}".format(self._job_info.owner))

        lines.extend([
            "   RunId: {}".format(self._runid),
            "   Start: {}".format(self._start),
            "    Stop: {}".format(self._stop),
            " ----------------- Detail ----------------- ",
            "       Errors: {}".format(self._error_count),
            "       Failed: {}".format(self._failure_count),
            "      Skipped: {}".format(self._skip_count),
            "       Passed: {}".format(self._pass_count),
            "        Total: {}".format(self._total_count),
            " ========================================== ",
            "   {}".format(self._summary["result"]),
            " ========================================== ",
            "",
            "OUTPUT PATH: {}".format(self._output_dir)
        ])

        if "MJR_SUMMARY_URL" in os.environ:
            summary_url = os.environ["MJR_SUMMARY_URL"]
            lines.append("SUMMARY URL: {}".format(summary_url))

        return lines

    def forward_summary_update(self, summary):
        return

    def get_summary_render_file_basename(self):
        return "testsummary.html"

    def initialize_report(self):

        self.update_render_environment()

        summary_html_source = self._render_info.summary_template
        summary_render_html_base = self.get_summary_render_file_basename()
        summary_render_html_dest = os.path.join(self._output_dir, summary_render_html_base)
        shutil.copy2(summary_html_source, summary_render_html_dest)

        self.catalog_output_directory()

        return

    def preview(self, result: ResultNode):
        """
            Provides a way to write a preview of a result to a result stream.  When a preview
            is written to the stream.  We record the result meta data as a preview but we do
            not include the result in any totals.

            :param result: A result object to be recorded.
        """
        raise NotOverloadedError("The 'preview' method must be overridden by derived 'ResultRecorder' objects.") from None

    def record(self, result: ResultNode):
        """
            Records an entry for the result object that is passed.

            :param result: A result object to be recorded.
        """
        raise NotOverloadedError("The 'record' method must be overridden by derived 'ResultRecorder' objects.") from None

    
    def clear_task_progress(self, task_ids: List[str]):

        self._lock.acquire()
        try:
            for tid in task_ids:
                if tid in self._running_tasks:
                    del self._running_tasks[tid]
        finally:
            self._lock.release()

        return

    def post_task_progress(self, progress_list: List[ProgressInfo]):

        fwd_summary = None

        self._lock.acquire()
        try:

            for progress in progress_list:

                if hasattr(progress, "status"):
                    if progress.status == ProgressCode.Completed:
                        del self._running_tasks[progress.id]
                    else:
                        self._running_tasks[progress.id] = progress.as_dict()    

            if self._forwarding_info is not None:
                now_time = datetime.now()
                if self._next_forward_at is None or now_time > self._next_forward_at:
                    fwd_summary = copy.deepcopy(self._summary)

        finally:
            self._lock.release()

        if fwd_summary is not None:
            self.forward_summary_update(fwd_summary)

        return


    def update_render_environment(self):
        """
            Called in order to publish resources required by the HTML presentation to
            the results directory tree.
            
            ..note: For Jenkins deployments and runs, you might want to override this method and
                    not publish for each run.
        """

        if self._render_info.static_resource_source is not None:
            static_resource_dest_dir = self._render_info.static_resource_destination
            static_resource_src_dir = self._render_info.static_resource_source

            for nxt_root, _, nxt_files in os.walk(static_resource_src_dir):
                for nf in nxt_files:
                    res_src_full: str = os.path.join(nxt_root, nf)
                    res_src_leaf = res_src_full[len(static_resource_src_dir):].lstrip(os.sep)
                    res_dest_full = os.path.join(static_resource_dest_dir, res_src_leaf)
                    if not os.path.exists(res_dest_full):
                        dest_dir = os.path.dirname(res_dest_full)
                        if not os.path.exists(dest_dir):
                            os.makedirs(dest_dir)
                        shutil.copy2(res_src_full, res_dest_full)

        return

    def update_summary(self): # pylint: disable=no-self-use
        """
            Writes out an update to the test run summary file.
        """
        raise NotOverloadedError("The 'update_summary' method must be overridden by derived 'ResultRecorder' objects.") from None

    