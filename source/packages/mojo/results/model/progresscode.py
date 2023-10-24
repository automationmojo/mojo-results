
from enum import Enum

class ProgressCode(str, Enum):

    Starting = "Starting"
    Running = "Running"
    Completed = "Completed"