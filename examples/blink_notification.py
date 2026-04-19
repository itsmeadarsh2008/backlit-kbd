"""
Example: Blink keyboard backlight as a notification (SOS in Morse code)
"""
import time
from backlit_kbd.factory import create_controller
from backlit_kbd import controller
from backlit_kbd.backends.mock import MockKeyboardBackend

MORSE_SOS = [0.2, 0.2, 0.2, 0.6, 0.6, 0.6, 0.2, 0.2, 0.2]  # S O S

try:
    ctrl = create_controller()
    max_brightness = ctrl.get_state().max_brightness
except Exception as e:
    print(f"[Example] WARNING: Could not access real keyboard backend ({e}). Using mock backend.")
    ctrl = controller.Controller(MockKeyboardBackend())
    max_brightness = ctrl.get_state().max_brightness

print("[Example] Blinking SOS notification...")
for duration in MORSE_SOS:
    ctrl.set_brightness(max_brightness)
    time.sleep(duration)
    ctrl.set_brightness(0)
    time.sleep(0.2)
print("[Example] Done.")
