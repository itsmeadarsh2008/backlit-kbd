# backlit-kbd

[![CI](https://img.shields.io/github/actions/workflow/status/itsmeadarsh2008/backlit-kbd/ci.yml?branch=main&label=tests)](https://github.com/itsmeadarsh2008/backlit-kbd/actions/workflows/ci.yml)
[![Publish](https://img.shields.io/github/actions/workflow/status/itsmeadarsh2008/backlit-kbd/publish.yml?branch=main&label=publish)](https://github.com/itsmeadarsh2008/backlit-kbd/actions/workflows/publish.yml)
[![PyPI version](https://img.shields.io/pypi/v/backlit-kbd)](https://pypi.org/project/backlit-kbd/)
[![Python](https://img.shields.io/pypi/pyversions/backlit-kbd)](https://pypi.org/project/backlit-kbd/)
[![License](https://img.shields.io/github/license/itsmeadarsh2008/backlit-kbd)](LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/backlit-kbd)](https://pypi.org/project/backlit-kbd/)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-support-yellow?logo=buymeacoffee)](https://buymeacoffee.com/itsmeadarsh)
[![Sponsor](https://img.shields.io/badge/GitHub%20Sponsors-support-pink?logo=githubsponsors)](https://github.com/sponsors/itsmeadarsh2008)

Beginner-friendly Python package to control keyboard backlight brightness.

It supports:
- Real Linux keyboard backlight devices (auto-discovered from sysfs)
- A mock backend for safe testing without touching laptop hardware

## What This Means

- If you use `--mock`, commands run in memory only (safe for learning).
- If you do not use `--mock`, the package tries real hardware automatically.
- You usually do not need `--device-path`.

## Installation

Step 1: Install from PyPI

```bash
pip install backlit-kbd
```

Step 2 (optional): Install local editable version for development

```bash
pip install -e .
```

Step 3 (optional): Install dev dependencies

```bash
pip install -e .[dev]
```

## Quick Start (Python)

Step 1: Import

```python
from backlit_kbd import NotificationBlinker, create_controller
```

Step 2: Create a safe controller (mock fallback)

```python
controller = create_controller(fallback_to_mock=True)
```

Step 3: Turn on brightness to 60%

```python
controller.turn_on(60.0)
```

Step 4: Blink for a notification

```python
controller.blink(count=3, on_ms=120, off_ms=120, level_percent=100.0)
```

Step 5: Use async notification manager

```python
blinker = NotificationBlinker(controller)
blinker.start("chat-message", count=5, on_ms=80, off_ms=120)
```

## CLI Guide (Beginner Friendly)

### 1) Check Current State

With mock backend:

```bash
backlit-kbd --mock info
```

With real hardware backend:

```bash
backlit-kbd info
```

### 2) Set Brightness by Raw Level

With mock backend:

```bash
backlit-kbd --mock set 2
```

With real hardware backend:

```bash
backlit-kbd set 2
```

### 3) Set Brightness by Percentage

With mock backend:

```bash
backlit-kbd --mock percent 75
```

With real hardware backend:

```bash
backlit-kbd percent 75
```

### 4) Increase and Decrease

Increase by default step (`1`):

```bash
backlit-kbd --mock inc
```

Increase by custom step:

```bash
backlit-kbd --mock inc 2
```

Decrease by custom step:

```bash
backlit-kbd --mock dec 2
```

Real hardware equivalents:

```bash
backlit-kbd inc
backlit-kbd inc 2
backlit-kbd dec 2
```

### 5) Turn On and Off

With mock backend:

```bash
backlit-kbd --mock on --percent 40
backlit-kbd --mock off
```

With real hardware backend:

```bash
backlit-kbd on --percent 40
backlit-kbd off
```

### 6) Blink Pattern (Synchronous)

With mock backend:

```bash
backlit-kbd --mock blink --count 4 --on-ms 100 --off-ms 100 --level-percent 100
```

With real hardware backend:

```bash
backlit-kbd blink --count 4 --on-ms 100 --off-ms 100 --level-percent 100
```

### 7) Notification Blink (Async-style Command)

With mock backend:

```bash
backlit-kbd --mock notify --name chat --count 5 --on-ms 80 --off-ms 120 --level-percent 100
```

With real hardware backend:

```bash
backlit-kbd notify --name chat --count 5 --on-ms 80 --off-ms 120 --level-percent 100
```

## Full CLI Commands

Global options:
- `--mock` Use in-memory backend (safe, no hardware writes)
- `--device-path PATH` Optional advanced override for a specific sysfs device

Commands:
- `info`
- `set <value>`
- `percent <value>`
- `inc [step]`
- `dec [step]`
- `on [--percent N]`
- `off`
- `blink [--count N --on-ms N --off-ms N --level-percent N]`
- `notify [--name NAME --count N --on-ms N --off-ms N --level-percent N]`

## Examples Folder

Scripts:
- `examples/blink_notification.py`
- `examples/brightness_wave.py`
- `examples/disco_light.py`

Run them:

```bash
python examples/blink_notification.py
```

```bash
python examples/brightness_wave.py
```

```bash
python examples/disco_light.py
```

## Testing

Run tests:

```bash
python -m pytest
```

If you are using the project virtual environment:

```bash
.venv/bin/pytest
```

## Troubleshooting

1. `Permission denied` on Linux real hardware mode:
- You may need proper privileges/udev rules to write to sysfs.

2. No device found in real hardware mode:
- Use `--mock` for learning/testing.
- Or use `create_controller(fallback_to_mock=True)` in Python.

3. Want safe practice mode always:
- Use `--mock` in CLI, or `force_mock=True` / `fallback_to_mock=True` in code.

## Release and Publish

This repo has GitHub Actions workflows:
- `CI` runs tests on push and pull request
- `Publish` builds and publishes to PyPI
- Uses `astral-sh/setup-uv`
- Uses PyPI Trusted Publishing (OIDC)

To publish a new version:
1. Update version in `pyproject.toml`
2. Create and push a tag like `v0.1.1`
3. Or publish a GitHub release

## Support

- Buy Me a Coffee: https://buymeacoffee.com/itsmeadarsh
- GitHub Sponsors (individual/company): https://github.com/sponsors/itsmeadarsh2008

## Contributing

- Start with `examples/`
- Check tests in `tests/`
- Open issues and PRs

## License

MIT License. Created by Adarsh Gourab Mahalik.
