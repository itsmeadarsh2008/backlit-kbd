"""
Example: Animate keyboard backlight in a smooth wave pattern.
"""
import time
import math
from backlit_kbd.factory import create_controller
from backlit_kbd import controller
from backlit_kbd.backends.mock import MockKeyboardBackend

try:
    ctrl = create_controller()
    max_brightness = ctrl.get_state().max_brightness
except Exception as e:
    print(f"[Example] WARNING: Could not access real keyboard backend ({e}). Using mock backend.")
    ctrl = controller.Controller(MockKeyboardBackend())
    max_brightness = ctrl.get_state().max_brightness

print("[Example] Running brightness wave animation. Press Ctrl+C to stop.")
t = 0.0
try:
    while True:
        level = (math.sin(t) + 1) / 2  # [0, 1]
        brightness = int(level * max_brightness)
        ctrl.set_brightness(brightness)
        print(f"Brightness: {brightness}/{max_brightness}", end='\r', flush=True)
        t += 0.1
        time.sleep(0.05)
except KeyboardInterrupt:
    print("\n[Example] Stopped.")
    ctrl.turn_on(50.0)
