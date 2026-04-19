import time

from backlit_kbd.backends.mock import MockKeyboardBackend
from backlit_kbd.controller import BacklitKeyboardController
from backlit_kbd.notifications import NotificationBlinker


def test_notification_worker_completes_and_cleans_up() -> None:
    controller = BacklitKeyboardController(
        MockKeyboardBackend(max_brightness=3, initial_brightness=1)
    )
    blinker = NotificationBlinker(controller)

    worker_name = "message"
    blinker.start(worker_name, count=2, on_ms=1, off_ms=1)

    timeout_at = time.time() + 2.0
    while worker_name in blinker.active() and time.time() < timeout_at:
        time.sleep(0.01)

    assert worker_name not in blinker.active()
    assert controller.get_state().brightness == 1


def test_stop_all_stops_running_workers() -> None:
    controller = BacklitKeyboardController(
        MockKeyboardBackend(max_brightness=3, initial_brightness=0)
    )
    blinker = NotificationBlinker(controller)

    blinker.start("a", count=100, on_ms=1, off_ms=1)
    blinker.start("b", count=100, on_ms=1, off_ms=1)

    blinker.stop_all(wait=True, timeout=1.0)

    assert blinker.active() == []
