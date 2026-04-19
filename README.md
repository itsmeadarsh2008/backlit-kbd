# backlit-kbd

[![CI](https://img.shields.io/github/actions/workflow/status/itsmeadarsh2008/backlit-kbd/ci.yml?branch=main&label=tests)](https://github.com/itsmeadarsh2008/backlit-kbd/actions/workflows/ci.yml)
[![Publish](https://img.shields.io/github/actions/workflow/status/itsmeadarsh2008/backlit-kbd/publish.yml?branch=main&label=publish)](https://github.com/itsmeadarsh2008/backlit-kbd/actions/workflows/publish.yml)
[![PyPI version](https://img.shields.io/pypi/v/backlit-kbd)](https://pypi.org/project/backlit-kbd/)
[![Python](https://img.shields.io/pypi/pyversions/backlit-kbd)](https://pypi.org/project/backlit-kbd/)
[![License](https://img.shields.io/github/license/itsmeadarsh2008/backlit-kbd)](LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/backlit-kbd)](https://pypi.org/project/backlit-kbd/)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-support-yellow?logo=buymeacoffee)](https://buymeacoffee.com/itsmeadarsh)
[![Sponsor](https://img.shields.io/badge/GitHub%20Sponsors-support-pink?logo=githubsponsors)](https://github.com/sponsors/itsmeadarsh2008)

A beginner-friendly Python package for controlling keyboard backlight devices.

Works on Linux laptops with sysfs backlight, and on any system with a mock backend for safe testing and learning. No hardware required.

## Features

- Control keyboard backlight brightness (set, percent, on/off)
- Notification-style blinking (sync and async)
- Background notification manager
- Mock backend for development/testing (no hardware needed)
- CLI and Python API
- Example scripts for experimentation

## Installation

Install locally:

```bash
pip install -e .
```

Install with developer dependencies:

```bash
pip install -e .[dev]
```

Install from PyPI:

```bash
pip install backlit-kbd
```

## Quick Start (Python)

```python
from backlit_kbd import NotificationBlinker, create_controller

# Always use fallback_to_mock=True for safe testing!
controller = create_controller(fallback_to_mock=True)

controller.turn_on(60.0)
controller.blink(count=3, on_ms=120, off_ms=120, level_percent=100.0)

blinker = NotificationBlinker(controller)
blinker.start("chat-message", count=5, on_ms=80, off_ms=120)
```

## CLI Usage

Try everything with the mock backend (no hardware needed):

```bash
# Show state
backlit-kbd --mock info

# Set by raw level
backlit-kbd --mock set 2

# Set by percentage
backlit-kbd --mock percent 75

# Blink for notification
backlit-kbd --mock blink --count 4 --on-ms 100 --off-ms 100
```

For a specific Linux device path:

```bash
backlit-kbd --device-path /sys/class/leds/asus::kbd_backlight info
```

## Examples

- `examples/blink_notification.py` - Blink SOS in Morse code
- `examples/brightness_wave.py` - Smooth wave animation
- `examples/disco_light.py` - Disco-style random brightness

Run with:

```bash
python examples/blink_notification.py
python examples/brightness_wave.py
python examples/disco_light.py
```

All examples automatically use the mock backend if hardware is unavailable.

## API Reference

- `create_controller(...)` returns a `BacklitKeyboardController`
- `BacklitKeyboardController`: `get_state()`, `set_brightness(value)`, `set_percent(percent)`, `increase(step=1)`, `decrease(step=1)`, `turn_on(percent=100.0)`, `turn_off()`, `blink(...)`
- `NotificationBlinker` manages named async blink notifications

## Testing

Run all tests:

```bash
pytest
```

## Release & Publish

This repository ships with two GitHub Actions workflows:

- `CI` (`.github/workflows/ci.yml`) runs tests on push and pull requests.
- `Publish` (`.github/workflows/publish.yml`) builds and publishes to PyPI on release publish, version tags (`v*`), or manual trigger.
- Workflows use `astral-sh/setup-uv` for package tooling and dependency management.

Recommended setup for publishing:

1. Create a PyPI project named `backlit-kbd`.
2. Configure PyPI Trusted Publisher (OIDC) for this GitHub repository.
3. Create a GitHub release or push a version tag like `v0.1.1`.

## Troubleshooting & Permissions

- Linux sysfs writes may require elevated permissions depending on distro/udev rules.
- For learning and testing, use the mock backend (`--mock` or `fallback_to_mock=True`).
- If no hardware backend is available and `fallback_to_mock=False`, backend creation raises `BackendUnavailableError`.

## Support

If this project helps you, you can support it here:

- Buy me a coffee: https://buymeacoffee.com/itsmeadarsh
- GitHub Sponsors (including company sponsorship): https://github.com/sponsors/itsmeadarsh2008

## Contributing

- Try the examples in `examples/` to get started.
- Add your own experiment by copying an example and modifying it.
- See `tests/` for API usage and edge cases.

## License

MIT License. Created by Adarsh Gourab Mahalik.
