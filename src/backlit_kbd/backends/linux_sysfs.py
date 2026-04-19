"""Linux sysfs backend for keyboard backlight devices."""

from __future__ import annotations

import threading
from pathlib import Path
from typing import Iterable

from .base import KeyboardBackend
from ..errors import BackendUnavailableError, InvalidBrightnessError


class LinuxSysfsKeyboardBackend(KeyboardBackend):
    """Backend that reads/writes keyboard backlight values via /sys/class/leds."""

    def __init__(self, device_path: str | Path) -> None:
        self._device_path = Path(device_path)
        self._brightness_file = self._device_path / "brightness"
        self._max_brightness_file = self._device_path / "max_brightness"
        self._lock = threading.Lock()

        if not self._brightness_file.exists() or not self._max_brightness_file.exists():
            raise BackendUnavailableError(
                f"Invalid keyboard backlight sysfs path: {self._device_path}"
            )

    @classmethod
    def discover_candidates(cls) -> list[Path]:
        """Return possible keyboard backlight sysfs paths."""
        base = Path("/sys/class/leds")
        if not base.exists():
            return []

        patterns: Iterable[str] = (
            "*kbd_backlight*",
            "*keyboard_backlight*",
            "*::kbd_backlight",
            "*input*::capslock",
        )

        found: list[Path] = []
        for pattern in patterns:
            for path in base.glob(pattern):
                if (path / "brightness").exists() and (path / "max_brightness").exists():
                    found.append(path)

        # Keep insertion order while removing duplicates.
        unique: dict[Path, None] = {}
        for path in found:
            unique[path] = None
        return list(unique.keys())

    @classmethod
    def auto(cls) -> "LinuxSysfsKeyboardBackend":
        """Create backend from first discovered sysfs candidate."""
        candidates = cls.discover_candidates()
        if not candidates:
            raise BackendUnavailableError(
                "No Linux keyboard backlight sysfs device discovered"
            )
        return cls(candidates[0])

    def is_available(self) -> bool:
        return self._brightness_file.exists() and self._max_brightness_file.exists()

    def get_brightness(self) -> int:
        with self._lock:
            return self._read_int(self._brightness_file)

    def get_max_brightness(self) -> int:
        with self._lock:
            return self._read_int(self._max_brightness_file)

    def set_brightness(self, value: int) -> None:
        max_value = self.get_max_brightness()
        if not 0 <= value <= max_value:
            raise InvalidBrightnessError(
                f"Brightness {value} is outside [0, {max_value}]"
            )

        with self._lock:
            try:
                self._brightness_file.write_text(f"{value}\n", encoding="utf-8")
            except PermissionError as exc:
                raise BackendUnavailableError(
                    "Permission denied writing keyboard brightness. "
                    "Try running with proper privileges."
                ) from exc

    @staticmethod
    def _read_int(path: Path) -> int:
        raw = path.read_text(encoding="utf-8").strip()
        try:
            return int(raw)
        except ValueError as exc:
            raise BackendUnavailableError(
                f"Unexpected non-integer value in {path}: {raw!r}"
            ) from exc
