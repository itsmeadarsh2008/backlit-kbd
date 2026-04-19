"""Factory helpers to create backlit keyboard controller instances."""

from __future__ import annotations

from .backends import LinuxSysfsKeyboardBackend, MockKeyboardBackend
from .controller import BacklitKeyboardController
from .errors import BackendUnavailableError


def create_controller(
    *,
    device_path: str | None = None,
    fallback_to_mock: bool = False,
    mock_max_brightness: int = 3,
    force_mock: bool = False,
) -> BacklitKeyboardController:
    """Create a controller with Linux sysfs backend and optional mock fallback.
    If force_mock is True, always use the mock backend and never attempt sysfs.
    """
    if force_mock:
        return BacklitKeyboardController(MockKeyboardBackend(max_brightness=mock_max_brightness))
    try:
        if device_path is not None:
            backend = LinuxSysfsKeyboardBackend(device_path)
        else:
            backend = LinuxSysfsKeyboardBackend.auto()
        return BacklitKeyboardController(backend)
    except BackendUnavailableError:
        if not fallback_to_mock:
            raise
        return BacklitKeyboardController(MockKeyboardBackend(max_brightness=mock_max_brightness))
