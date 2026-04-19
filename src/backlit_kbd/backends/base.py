"""Backend interface for keyboard backlight control."""

from __future__ import annotations

from abc import ABC, abstractmethod


class KeyboardBackend(ABC):
    """Abstract backend contract for keyboard backlight operations."""

    @abstractmethod
    def is_available(self) -> bool:
        """Return True when the backend can communicate with hardware."""

    @abstractmethod
    def get_brightness(self) -> int:
        """Return current brightness value."""

    @abstractmethod
    def get_max_brightness(self) -> int:
        """Return maximum supported brightness value."""

    @abstractmethod
    def set_brightness(self, value: int) -> None:
        """Set brightness to an integer value within backend-specific range."""
