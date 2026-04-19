"""
Example: Disco light effect for keyboard backlight.
Rapidly cycles brightness in a random pattern for a party/disco effect.
"""
import time
import random
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

print("[Example] Disco light effect! Press Ctrl+C to stop.")
try:
    while True:
        brightness = random.randint(0, max_brightness)
        ctrl.set_brightness(brightness)
        print(f"Disco brightness: {brightness}/{max_brightness}", end='\r', flush=True)
        time.sleep(random.uniform(0.03, 0.15))
except KeyboardInterrupt:
    print("\n[Example] Stopped.")
    ctrl.turn_on(50.0)
