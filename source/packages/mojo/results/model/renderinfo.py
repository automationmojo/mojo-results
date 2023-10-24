"""
.. module:: renderinfo
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the :class:`RenderInfo` dataclass used to contain and pass
               result rendering information

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

from dataclasses import dataclass

@dataclass
class RenderInfo:

    title: str # A title to associated with the summary for the test results.
    summary_filename: str # The full path to the summary file where the test run summary should be written to.
    summary_template: str # The full path to the summary file source template
    result_filename: str # The full path to the results file where the test run results should be written to.
    static_resource_source: str # The source folder for the static render resources
    static_resource_destination: str # The destination folder for static render resources
