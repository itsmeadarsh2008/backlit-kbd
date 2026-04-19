"""Command-line interface for backlit keyboard operations."""

from __future__ import annotations

import argparse
import time

from .factory import create_controller
from .notifications import NotificationBlinker


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(description="Control keyboard backlit brightness")
    parser.add_argument(
        "--device-path",
        help="Sysfs LED device path (e.g. /sys/class/leds/asus::kbd_backlight)",
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Fallback to in-memory backend if hardware backend is unavailable",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("info", help="Show current brightness state")

    set_parser = subparsers.add_parser("set", help="Set raw brightness level")
    set_parser.add_argument("value", type=int)

    percent_parser = subparsers.add_parser("percent", help="Set brightness percentage")
    percent_parser.add_argument("value", type=float)

    inc_parser = subparsers.add_parser("inc", help="Increase brightness")
    inc_parser.add_argument("step", type=int, nargs="?", default=1)

    dec_parser = subparsers.add_parser("dec", help="Decrease brightness")
    dec_parser.add_argument("step", type=int, nargs="?", default=1)

    subparsers.add_parser("off", help="Turn keyboard backlight off")

    on_parser = subparsers.add_parser("on", help="Turn keyboard backlight on")
    on_parser.add_argument("--percent", type=float, default=100.0)

    blink_parser = subparsers.add_parser("blink", help="Run synchronous blink pattern")
    blink_parser.add_argument("--count", type=int, default=3)
    blink_parser.add_argument("--on-ms", type=int, default=150)
    blink_parser.add_argument("--off-ms", type=int, default=150)
    blink_parser.add_argument("--level-percent", type=float, default=100.0)

    notify_parser = subparsers.add_parser(
        "notify", help="Run asynchronous notification blinker and wait for completion"
    )
    notify_parser.add_argument("--name", default="default")
    notify_parser.add_argument("--count", type=int, default=3)
    notify_parser.add_argument("--on-ms", type=int, default=150)
    notify_parser.add_argument("--off-ms", type=int, default=150)
    notify_parser.add_argument("--level-percent", type=float, default=100.0)

    return parser


def _print_state(prefix: str, brightness: int, max_brightness: int, percent: float) -> None:
    print(
        f"{prefix}: brightness={brightness}/{max_brightness} "
        f"({percent:.1f}%)"
    )


def main(argv: list[str] | None = None) -> int:
    """Run CLI entrypoint."""
    parser = build_parser()
    args = parser.parse_args(argv)

    controller = create_controller(
        device_path=args.device_path,
        fallback_to_mock=args.mock,
        force_mock=args.mock,
    )

    if args.command == "info":
        state = controller.get_state()
        _print_state("state", state.brightness, state.max_brightness, state.percent)
        return 0

    if args.command == "set":
        state = controller.set_brightness(args.value)
        _print_state("updated", state.brightness, state.max_brightness, state.percent)
        return 0

    if args.command == "percent":
        state = controller.set_percent(args.value)
        _print_state("updated", state.brightness, state.max_brightness, state.percent)
        return 0

    if args.command == "inc":
        state = controller.increase(args.step)
        _print_state("updated", state.brightness, state.max_brightness, state.percent)
        return 0

    if args.command == "dec":
        state = controller.decrease(args.step)
        _print_state("updated", state.brightness, state.max_brightness, state.percent)
        return 0

    if args.command == "off":
        state = controller.turn_off()
        _print_state("updated", state.brightness, state.max_brightness, state.percent)
        return 0

    if args.command == "on":
        state = controller.turn_on(args.percent)
        _print_state("updated", state.brightness, state.max_brightness, state.percent)
        return 0

    if args.command == "blink":
        state = controller.blink(
            args.count,
            on_ms=args.on_ms,
            off_ms=args.off_ms,
            level_percent=args.level_percent,
        )
        _print_state("updated", state.brightness, state.max_brightness, state.percent)
        return 0

    if args.command == "notify":
        blinker = NotificationBlinker(controller)
        blinker.start(
            args.name,
            count=args.count,
            on_ms=args.on_ms,
            off_ms=args.off_ms,
            level_percent=args.level_percent,
        )
        while args.name in blinker.active():
            time.sleep(0.01)
        state = controller.get_state()
        _print_state("updated", state.brightness, state.max_brightness, state.percent)
        return 0

    parser.error("Unknown command")
    return 2
