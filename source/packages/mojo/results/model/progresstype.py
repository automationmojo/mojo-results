
from enum import Enum

class ProgressType(str, Enum):

    NumericRange = "NumericRange"
    Sequential = "Sequential"
    TimeSpan = "TimeSpan"
