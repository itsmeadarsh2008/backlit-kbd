"""Shared data types used by the package."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class KeyboardState:
    """Snapshot of current keyboard backlight state."""

    brightness: int
    max_brightness: int

    @property
    def percent(self) -> float:
        """Return current brightness as percentage in range [0.0, 100.0]."""
        if self.max_brightness <= 0:
            return 0.0
        return (self.brightness / self.max_brightness) * 100.0
