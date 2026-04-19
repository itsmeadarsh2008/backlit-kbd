from backlit_kbd.backends.mock import MockKeyboardBackend
from backlit_kbd.controller import BacklitKeyboardController
from backlit_kbd.errors import InvalidBrightnessError


def test_set_percent_rounds_within_range() -> None:
    controller = BacklitKeyboardController(
        MockKeyboardBackend(max_brightness=10, initial_brightness=0)
    )

    state = controller.set_percent(55.0)

    assert state.brightness == 6
    assert state.max_brightness == 10


def test_set_brightness_outside_range_raises() -> None:
    controller = BacklitKeyboardController(
        MockKeyboardBackend(max_brightness=3, initial_brightness=1)
    )

    try:
        controller.set_brightness(10)
        raised = False
    except InvalidBrightnessError:
        raised = True

    assert raised is True


def test_blink_restores_previous_brightness() -> None:
    controller = BacklitKeyboardController(
        MockKeyboardBackend(max_brightness=4, initial_brightness=2)
    )

    state = controller.blink(count=2, on_ms=1, off_ms=1, level_percent=100.0, restore=True)

    assert state.brightness == 2
    assert controller.get_state().brightness == 2
