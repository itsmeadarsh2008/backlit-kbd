"""In-memory backend used for testing and local development."""

from __future__ import annotations

import threading

from .base import KeyboardBackend
from ..errors import InvalidBrightnessError


class MockKeyboardBackend(KeyboardBackend):
    """Simple in-memory backend with thread-safe brightness storage."""

    def __init__(self, max_brightness: int = 3, initial_brightness: int = 0) -> None:
        if max_brightness <= 0:
            raise ValueError("max_brightness must be greater than 0")
        if not 0 <= initial_brightness <= max_brightness:
            raise ValueError("initial_brightness must be within [0, max_brightness]")

        self._max_brightness = max_brightness
        self._brightness = initial_brightness
        self._lock = threading.Lock()

    def is_available(self) -> bool:
        return True

    def get_brightness(self) -> int:
        with self._lock:
            return self._brightness

    def get_max_brightness(self) -> int:
        return self._max_brightness

    def set_brightness(self, value: int) -> None:
        if not 0 <= value <= self._max_brightness:
            raise InvalidBrightnessError(
                f"Brightness {value} is outside [0, {self._max_brightness}]"
            )
        with self._lock:
            self._brightness = value
