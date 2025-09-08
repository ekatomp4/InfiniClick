import ctypes
import time
import threading
import sys
import keyboard
from pynput import mouse

# ==============================
# CONFIG: Set toggle input here
# ==============================
TOGGLE_INPUT = "x2"   # options: "enter", "q", "x1", "x2", "left", "right", "middle"
CPS = 10              # clicks per second
DOUBLE_CLICK = True   # perform a second click after DEBOUNCE_TIME
CLICK_TIME = 0.01     # time between clicks
DEBOUNCE_TIME = 0.1   # time between double clicks
CLOSEKEY = ";"        # key to kill the script
# ==============================

# Load user32 for clicking
user32 = ctypes.windll.user32
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP   = 0x0004

is_active = False
click_thread = None

def click_loop():
    while is_active:
        # First click
        user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(CLICK_TIME)
        user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

        if DOUBLE_CLICK:
            # Immediately do a second click
            time.sleep(CLICK_TIME)  # tiny gap between clicks
            user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            time.sleep(CLICK_TIME)
            user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

        # Delay before repeating the cycle
        time.sleep(1 / CPS)

def start_clicking():
    global is_active, click_thread
    if not is_active:
        is_active = True
        click_thread = threading.Thread(target=click_loop, daemon=True)
        click_thread.start()
        print("Clicking started")

def stop_clicking():
    global is_active
    is_active = False
    print("Clicking stopped")

def toggle_clicking():
    global is_active
    if is_active:
        stop_clicking()
    else:
        start_clicking()

def close_program():
    global is_active
    is_active = False
    print("Exiting program...")
    sys.exit(0)

# ---------------------------------
# Input handling
# ---------------------------------
def setup_input():
    # Close hotkey (keyboard only)
    keyboard.add_hotkey(CLOSEKEY, close_program)

    # If TOGGLE_INPUT is a keyboard key
    if TOGGLE_INPUT.lower() not in ["x1", "x2", "left", "right", "middle"]:
        keyboard.on_press_key(TOGGLE_INPUT.lower(), lambda e: toggle_clicking())
        print(f"Press '{TOGGLE_INPUT}' anywhere to toggle autoclicker. Press '{CLOSEKEY}' to quit.")
        keyboard.wait()  # wait for events

    # If TOGGLE_INPUT is a mouse button
    else:
        btn_map = {
            "left": mouse.Button.left,
            "right": mouse.Button.right,
            "middle": mouse.Button.middle,
            "x1": mouse.Button.x1,
            "x2": mouse.Button.x2,
        }

        def on_click(x, y, button, pressed):
            if button == btn_map[TOGGLE_INPUT.lower()] and pressed:
                toggle_clicking()

        print(f"Press mouse button '{TOGGLE_INPUT}' to toggle autoclicker. Press '{CLOSEKEY}' to quit.")
        with mouse.Listener(on_click=on_click) as listener:
            listener.join()

# Run input setup
setup_input()
