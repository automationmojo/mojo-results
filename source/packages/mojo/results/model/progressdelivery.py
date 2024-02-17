
from typing import List, Protocol

from dataclasses import dataclass

from mojo.results.model.progressinfo import ProgressInfo


class ProgressDeliveryMethod:
    SUMMARY_PULL_PROGRESS = "summary-pull-progress"



class TaskingProgressCallback(Protocol):

    def __call__(self, progress: List[ProgressInfo]) -> None: ...


@dataclass
class SummaryProgressDelivery:
    progress_interval: float
    progress_callback: TaskingProgressCallback

