"""
.. module:: jobcontainer
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the :class:`JobContainer` object used to serve as a
               tree node container for children of type JOB.

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


from mojo.results.model.resulttype import ResultType
from mojo.results.model.resultcontainer import ResultContainer

class JobContainer(ResultContainer):
    """
        The :class:`JobContainer` instances are container nodes that are used to link result nodes in the
        result tree.  The :class:`JobContainer` node is the base node for the tree.
    """
    def __init__(self, inst_id: str, name: str):
        """
            Creates an instance of a result container.

            :param inst_id: The unique identifier to link this result container with its children.
            :param name: The name of the result container.
        """
        super().__init__(inst_id, name, ResultType.JOB, parent_inst=None)
        return
