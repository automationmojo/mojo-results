
from enum import Enum

class ProgressCode(str, Enum):

    Completed = "Completed"
    Errored = "Errored"
    Failed = "Failed"
    NotStarted = "NotStarted"
    Paused = "Paused"
    Running = "Running"
