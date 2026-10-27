"""Device-independent interface consumed by the dashboard."""

from abc import ABC, abstractmethod


class EMGConnection(ABC):
    def __init__(self, t_min: float, t_max: float):
        """Accept window limits in milliseconds; expose them in seconds."""
        self.t_min = t_min / 1000
        self.t_max = t_max / 1000

    @abstractmethod
    def start(self) -> None:
        """Start acquisition in the background without blocking the caller."""

    @abstractmethod
    def stop(self) -> None:
        """Stop acquisition and release the device's resources."""

    @abstractmethod
    def get_connection(self) -> bool:
        """Return whether the device is connected."""

    @abstractmethod
    def get_status(self) -> bool:
        """Return whether a measurement is active."""

    @abstractmethod
    def get_sampling_rate(self) -> int:
        """Return the sampling rate in Hz, or zero before it is known."""

    @abstractmethod
    def get_triggered_window(self) -> list[list[float]]:
        """Return a thread-safe history snapshot, oldest first, in microvolts.

        Windows span [t_min, t_max) relative to the trigger. Repeated calls
        retain the history; return an empty list while acquisition is inactive.
        """
