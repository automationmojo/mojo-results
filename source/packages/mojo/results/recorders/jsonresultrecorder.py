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


from typing import Optional

import json

from datetime import datetime


from mojo.results.model.buildinfo import BuildInfo
from mojo.results.model.jobinfo import JobInfo
from mojo.results.model.pipelineinfo import PipelineInfo
from mojo.results.model.renderinfo import RenderInfo

from mojo.results.recorders.resultrecorder import ResultRecorder


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

    def update_summary(self):
        """
            Writes out an update to the test run summary file.
        """

        with open(self._render_info.summary_filename, 'w') as sout:
            json.dump(self._summary, sout, indent=4)

        return
    