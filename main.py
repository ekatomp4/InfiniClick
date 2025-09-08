import ctypes
import time
import threading
import sys
import keyboard
import random
from pynput import mouse
import pyautogui


# ==============================
# CONFIG
# ==============================
TOGGLE_INPUT = "x2"          # "enter", "q", "x1", "x2", "left", "right", "middle"
CLOSEKEY = ";"               # key to kill the script
WHILE_HELD = True

CPS = 10                     # average clicks per second
CPS_VARIANCE = 2             # +/- CPS variance to randomize human-like clicks

BURST_AMOUNT = 2          # fixed number of clicks in a row
BURST_PAUSE = 0.1         # gap after each burst

DOUBLE_CLICK_CHANCE = 30

JITTER_AMOUNT = 30
JITTER_CHANCE = 50
JITTER_MIN_DUR = 0.07
JITTER_MAX_DUR = 0.2
is_jittering = False

IS_RIGHT_CLICK = False
# ==============================

# Load user32 for clicking
user32 = ctypes.windll.user32
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP   = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP   = 0x0010

is_active = False
click_thread = None

AVG_CPS = CPS + random.uniform(-CPS_VARIANCE, CPS_VARIANCE)
STD_CPS = CPS_VARIANCE


def do_click():
    if IS_RIGHT_CLICK:
        user32.mouse_event(MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
        user32.mouse_event(MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
    else:
        user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

def jitter_mouse():
    global is_jittering
    if is_jittering:
        return
    
    is_jittering = True

    x = random.uniform(-JITTER_AMOUNT, JITTER_AMOUNT)
    y = random.uniform(-JITTER_AMOUNT, JITTER_AMOUNT)
    # Move cursor smoothly in one call
    current_x, current_y = pyautogui.position()
    dur = random.uniform(JITTER_MIN_DUR, JITTER_MAX_DUR)
    pyautogui.moveTo(current_x + x, current_y + y, duration=dur)

    is_jittering = False

def maybe_jitter():
    if random.randint(0, 100) < JITTER_CHANCE:
        # Run jitter_mouse in a separate thread
        threading.Thread(target=jitter_mouse, daemon=True).start()


def click_loop():
    global is_active
    while is_active:
        # Jitter mouse
        maybe_jitter()


        # Perform the burst
        for _ in range(BURST_AMOUNT):
            do_click()

            # Double-click chance
            if random.randint(0, 100) < DOUBLE_CLICK_CHANCE:
                do_click()
            
            # Randomized delay based on CPS variance for each click
            cps_this_click = max(1.0, random.gauss(CPS, CPS_VARIANCE))
            delay = 1.0 / cps_this_click
            time.sleep(delay)

        # Pause after the burst
        time.sleep(BURST_PAUSE)


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
        if WHILE_HELD:
            # Start clicking on press, stop on release
            keyboard.on_press_key(TOGGLE_INPUT.lower(), lambda e: start_clicking())
            keyboard.on_release_key(TOGGLE_INPUT.lower(), lambda e: stop_clicking())
            print(f"Hold '{TOGGLE_INPUT}' to click. Press '{CLOSEKEY}' to quit.")
            keyboard.wait()  # wait for events
        else:
            # Toggle behavior
            keyboard.on_press_key(TOGGLE_INPUT.lower(), lambda e: toggle_clicking())
            print(f"Press '{TOGGLE_INPUT}' to toggle autoclicker. Press '{CLOSEKEY}' to quit.")
            keyboard.wait()

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
            if button == btn_map[TOGGLE_INPUT.lower()]:
                if WHILE_HELD:
                    if pressed:
                        start_clicking()
                    else:
                        stop_clicking()
                else:
                    if pressed:
                        toggle_clicking()

        print(f"Press mouse button '{TOGGLE_INPUT}' to click. Press '{CLOSEKEY}' to quit.")
        with mouse.Listener(on_click=on_click) as listener:
            listener.join()

# Run input setup
setup_input()
