import keyboard
from pynput import mouse
from modules.clicker_core import Clicker
import time

STOP_ALL = False  # global flag to exit loop

def setup_inputs(bindings):
    global STOP_ALL
    clickers = [Clicker(cfg) for cfg in bindings]

    btn_map = {
        "left": mouse.Button.left,
        "right": mouse.Button.right,
        "middle": mouse.Button.middle,
        "x1": mouse.Button.x1,
        "x2": mouse.Button.x2,
    }

    # Keyboard bindings
    for clicker in clickers:
        key = clicker.config["TOGGLE_INPUT"].lower()
        if key not in btn_map:  # keyboard binding
            if clicker.config["WHILE_HELD"]:
                keyboard.on_press_key(key, lambda e, c=clicker: c.start())
                keyboard.on_release_key(key, lambda e, c=clicker: c.stop())
                print(f"[{key}] Hold to click.")
            else:
                keyboard.on_press_key(key, lambda e, c=clicker: c.toggle())
                print(f"[{key}] Toggle mode.")

    # Mouse bindings
    def on_click(x, y, button, pressed):
        for clicker in clickers:
            key = clicker.config["TOGGLE_INPUT"].lower()
            if key in btn_map and button == btn_map[key]:
                if clicker.config["WHILE_HELD"]:
                    if pressed:
                        clicker.start()
                    else:
                        clicker.stop()
                else:
                    if pressed:
                        clicker.toggle()

    mouse_listener = mouse.Listener(on_click=on_click)
    mouse_listener.start()
    print("Mouse bindings ready.")

    # Emergency stop hotkey
    keyboard.add_hotkey("i+c+s", lambda: stop_all(clickers))

    print("Press I+C+S to stop all clickers and return to menu.")

    # Instead of keyboard.wait(), just loop and sleep
    while not STOP_ALL:
        time.sleep(0.1)

    # After STOP_ALL is True, reset flag and return
    STOP_ALL = False
    print("Exiting clicker loop.")


def stop_all(clickers):
    global STOP_ALL
    STOP_ALL = True
    for c in clickers:
        c.stop()
