"""High-level controller API for keyboard backlight operations."""

from __future__ import annotations

import time
from threading import Event

from .backends.base import KeyboardBackend
from .errors import InvalidBrightnessError
from .types import KeyboardState


class BacklitKeyboardController:
    """Primary API surface for backlight state and brightness controls."""

    def __init__(self, backend: KeyboardBackend) -> None:
        if not backend.is_available():
            raise ValueError("Provided backend is not available")
        self._backend = backend

    @property
    def backend(self) -> KeyboardBackend:
        """Expose underlying backend for advanced integrations."""
        return self._backend

    def get_state(self) -> KeyboardState:
        """Return current brightness snapshot."""
        return KeyboardState(
            brightness=self._backend.get_brightness(),
            max_brightness=self._backend.get_max_brightness(),
        )

    def set_brightness(self, value: int) -> KeyboardState:
        """Set brightness using raw backend units."""
        max_brightness = self._backend.get_max_brightness()
        if not 0 <= value <= max_brightness:
            raise InvalidBrightnessError(
                f"Brightness {value} is outside [0, {max_brightness}]"
            )
        self._backend.set_brightness(value)
        return self.get_state()

    def set_percent(self, percent: float) -> KeyboardState:
        """Set brightness based on percentage [0.0, 100.0]."""
        if not 0.0 <= percent <= 100.0:
            raise InvalidBrightnessError(
                f"Brightness percent {percent} must be in range [0.0, 100.0]"
            )

        max_brightness = self._backend.get_max_brightness()
        value = round((percent / 100.0) * max_brightness)
        return self.set_brightness(value)

    def increase(self, step: int = 1) -> KeyboardState:
        """Increase brightness by a given step without exceeding max."""
        if step <= 0:
            raise ValueError("step must be greater than 0")
        state = self.get_state()
        return self.set_brightness(min(state.max_brightness, state.brightness + step))

    def decrease(self, step: int = 1) -> KeyboardState:
        """Decrease brightness by a given step without going below zero."""
        if step <= 0:
            raise ValueError("step must be greater than 0")
        state = self.get_state()
        return self.set_brightness(max(0, state.brightness - step))

    def turn_off(self) -> KeyboardState:
        """Turn keyboard backlight fully off."""
        return self.set_brightness(0)

    def turn_on(self, percent: float = 100.0) -> KeyboardState:
        """Turn keyboard backlight on with desired brightness percent."""
        return self.set_percent(percent)

    def blink(
        self,
        count: int,
        *,
        on_ms: int = 150,
        off_ms: int = 150,
        level_percent: float = 100.0,
        restore: bool = True,
        stop_event: Event | None = None,
    ) -> KeyboardState:
        """Blink keyboard backlight synchronously for notification-style effects."""
        if count <= 0:
            raise ValueError("count must be greater than 0")
        if on_ms < 0 or off_ms < 0:
            raise ValueError("on_ms/off_ms cannot be negative")

        previous = self.get_state()

        for _ in range(count):
            if stop_event is not None and stop_event.is_set():
                break
            self.set_percent(level_percent)
            time.sleep(on_ms / 1000.0)
            if stop_event is not None and stop_event.is_set():
                break
            self.turn_off()
            time.sleep(off_ms / 1000.0)

        if restore:
            return self.set_brightness(previous.brightness)
        return self.get_state()
