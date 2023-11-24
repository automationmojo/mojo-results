"""
.. module:: testcontainer
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the :class:`TestContainer` object used to serve as a
               tree node container for children of type TEST.

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

class TestContainer(ResultContainer):
    """
        The :class:`TestContainer` instances are container nodes that are used to link result nodes in the
        result tree.  The :class:`TestsContainer` nodes do not contain result data but link data so the data can
        be computed on demand.
    """
    def __init__(self, inst_id: str, name: str, parent_inst: str):
        """
            Creates an instance of a result container.

            :param inst_id: The unique identifier to link this result container with its children.
            :param name: The name of the result container.
            :param parent_inst: The unique identifier fo this result nodes parent.
        """
        super().__init__(inst_id, name, ResultType.TEST_CONTAINER, parent_inst=parent_inst)
        return
