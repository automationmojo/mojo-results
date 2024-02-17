"""
.. module:: jsonresultrecorder
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the :class:`JsonResultRecorder` object.

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


from typing import Any, Optional

import json

from datetime import datetime

from mojo.xmods.jsos import CHAR_RECORD_SEPERATOR

from mojo.results.model.buildinfo import BuildInfo
from mojo.results.model.jobinfo import JobInfo
from mojo.results.model.pipelineinfo import PipelineInfo
from mojo.results.model.renderinfo import RenderInfo

from mojo.results.model.resultcode import ResultCode
from mojo.results.model.resultnode import ResultNode
from mojo.results.model.resulttype import ResultType

from mojo.results.recorders.resultrecorder import ResultRecorder


class JsonResultEncoder(json.JSONEncoder):

    def default(self, obj) -> Any:

        cval = None

        if isinstance(obj, datetime):
            cval = obj.isoformat()
        else:
            cval = json.JSONEncoder.default(self, obj)

        return cval




class JsonResultRecorder(ResultRecorder):
    """
        The :class:`JsonResultRecorder` object records test results in JSON format.
    """
    def __init__(self, *, runid: str, start: datetime, render_info: RenderInfo,
                 apod: Optional[str] = None, build_info: Optional[BuildInfo] = None,
                 pipeline_info: Optional[PipelineInfo] = None, job_info: Optional[JobInfo] = None):
        """
            Initializes the :class:`JsonResultRecorder` object for recording test results for
            a test run.

            :param runid: The uuid string that identifies a set of test results.
            :param start: The date and time of the start of the test run.
            :param render_info: Automation results rendering info
            :param apod: Optional name of an automation pod that the automation run is running on.
            :param build_info: Optional build information to associate with an automation run.
            :param pipeline_info: Optional pipeline information to associate with an automation run.
            :param job_info: Optional job information to associate with an automation run.
        """
        super(JsonResultRecorder, self).__init__(runid=runid, start=start, render_info=render_info, apod=apod,
                                                 build_info=build_info, pipeline_info=pipeline_info, job_info=job_info)
        return

    def preview(self, result: ResultNode):
        """
            Provides a way to write a preview of a result to a result stream.  When a preview
            is written to the stream.  We record the result meta data as a preview but we do
            not include the result in any totals.

            :param result: A result object to be recorded.
        """

        json_str = result.to_json(is_preview=True)

        self._rout.write(CHAR_RECORD_SEPERATOR)
        self._rout.write(json_str)
        self._rout.flush()

        self.catalog_output_directory()

        return

    def record(self, result: ResultNode):
        """
            Records an entry for the result object that is passed.

            :param result: A result object to be recorded.
        """
        
        json_str = result.to_json(is_preview=False)

        self._rout.write(CHAR_RECORD_SEPERATOR)
        self._rout.write(json_str)
        self._rout.flush()

        self._lock.acquire()
        try:
            if result.result_type == ResultType.TEST:
                self._total_count += 1

                result_code = result.result_code
                if result_code == ResultCode.PASSED:
                    self._pass_count += 1
                elif result_code == ResultCode.ERRORED:
                    self._error_count += 1
                elif result_code == ResultCode.FAILED:
                    self._failure_count += 1
                elif result_code == ResultCode.SKIPPED:
                    self._skip_count += 1
                else:
                    self._unknown_count += 1
        finally:
            self._lock.release()

        self.catalog_output_directory()

        return

    def update_summary(self):
        """
            Writes out an update to the test run summary file.
        """

        with open(self._render_info.summary_filename, 'w') as sout:
            json.dump(self._summary, sout, indent=4, cls=JsonResultEncoder)

        self.catalog_output_directory()

        return
    