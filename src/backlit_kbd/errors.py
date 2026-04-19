"""Custom exceptions for backlit keyboard control."""


class BacklitKeyboardError(Exception):
    """Base exception for the package."""


class BackendUnavailableError(BacklitKeyboardError):
    """Raised when no usable keyboard backlight backend is available."""


class InvalidBrightnessError(BacklitKeyboardError):
    """Raised when a brightness value is outside the allowed range."""


class NotificationAlreadyRunningError(BacklitKeyboardError):
    """Raised when trying to start a duplicate notification worker."""
