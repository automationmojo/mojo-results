"""
.. module:: progressinfo
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the :class:`ProgressInfo` class which is used to report task progress.

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


from dataclasses import dataclass
from datetime import datetime


from mojo.results.model.progresscode import ProgressCode
from mojo.results.model.progresstype import ProgressType


@dataclass
class ProgressInfo:

    id: str
    category: str
    moniker: str
    ptype: ProgressType
    range_min: str
    range_max: str
    position: str
    status: ProgressCode
    when: datetime
    data: Optional[dict] = None

    def as_dict(self) -> dict:

        rtnval = {
            "id": self.id,
            "category": self.category,
            "moniker": self.moniker,
            "ptype": self.ptype.name,
            "range_min": self.range_min,
            "range_max": self.range_max,
            "position": self.position,
            "status": self.status.name,
            "when": self.when.isoformat()
        }

        if self.data is not None:
            rtnval["data"] = self.data
        else:
            rtnval["data"] = {}

        return rtnval
    
    @classmethod
    def from_dict(data: dict) -> "ProgressInfo":
        when = datetime.fromisoformat(data["when"])

        inst = ProgressInfo(data["id"], data["category"], data["moniker"], data["ptype"], data["range_min"],
                            data["range_max"], data["position"], data["status"], when, data["data"])
        return inst
    
    def __repr__(self):
        reprval = repr(self.as_dict())
        return reprval