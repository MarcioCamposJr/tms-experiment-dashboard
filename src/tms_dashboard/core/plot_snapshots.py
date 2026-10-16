"""Read-only data published for dashboard plots, independent of communication flags."""

from dataclasses import dataclass


@dataclass(frozen=True)
class TimeSeriesSnapshot:
    revision: int
    displacement_time: tuple[float, ...]
    displacement: tuple[tuple[float, ...], ...]
    rotation_time: tuple[float, ...]
    rotation: tuple[tuple[float, ...], ...]
    trigger_times: tuple[float, ...]
