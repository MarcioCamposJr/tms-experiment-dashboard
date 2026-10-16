"""Read-only data published for dashboard plots, independent of communication flags."""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class TimeSeriesSnapshot:
    revision: int
    displacement_time: tuple[float, ...]
    displacement: tuple[tuple[float, ...], ...]
    rotation_time: tuple[float, ...]
    rotation: tuple[tuple[float, ...], ...]
    trigger_times: tuple[float, ...]


@dataclass(frozen=True)
class MepPlotSnapshot:
    revision: int
    windows: tuple[np.ndarray, ...] = ()
    peak_to_peak: tuple[float, ...] = ()
    t_min: float = 0.0
    t_max: float = 0.0
