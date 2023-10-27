
from enum import Enum

class ProgressCode(str, Enum):

    Completed = "Completed"
    Errored = "Errored"
    NotStarted = "NotStarted"
    Paused = "Paused"
    Running = "Running"
