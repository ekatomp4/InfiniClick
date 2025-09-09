import ctypes
import time
import threading
import random
import pyautogui

# Windows API mouse events
user32 = ctypes.windll.user32
MOUSEEVENTF_LEFTDOWN  = 0x0002
MOUSEEVENTF_LEFTUP    = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP   = 0x0010

class Clicker:
    def __init__(self, config):
        self.config = config
        self.is_active = False
        self.click_thread = None
        self.current_clicks = 0
        self.current_side = 0
        self.current_target_cps = config["CPS"] + random.uniform(-config["CPS_VARIANCE"], config["CPS_VARIANCE"])

    def do_click(self, right_click=False):
        if right_click:
            user32.mouse_event(MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
            user32.mouse_event(MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
        else:
            user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    def jitter_mouse(self):
        if random.randint(0, 100) < self.config["JITTER_CHANCE"]:
            x = random.uniform(-self.config["JITTER_AMOUNT"], self.config["JITTER_AMOUNT"])
            y = random.uniform(-self.config["JITTER_AMOUNT"], self.config["JITTER_AMOUNT"])
            cur_x, cur_y = pyautogui.position()
            dur = random.uniform(self.config["JITTER_MIN_DUR"], self.config["JITTER_MAX_DUR"])
            pyautogui.moveTo(cur_x + x, cur_y + y, duration=dur)

    def click_loop(self):
        while self.is_active:
            if self.config["IS_BLOCK_HITTING"]:
                # Alternate hit/block
                self.do_click(right_click=(self.current_side == 1))
                if self.current_side == 0:
                    self.current_side = 1 if random.random() < self.config["BLOCK_TO_HIT_RATIO"] else 0
                    delay = 1.0 / self.config["HIT_CPS"]
                else:
                    self.current_side = 0
                    delay = 1.0 / self.config["BLOCK_CPS"]
                time.sleep(delay)
                continue

            # Maybe jitter
            self.jitter_mouse()

            # Burst clicks
            for _ in range(self.config["BURST_AMOUNT"]):
                start_click = time.perf_counter()
                self.do_click()
                if random.randint(0, 100) < self.config["DOUBLE_CLICK_CHANCE"]:
                    self.do_click()

                cps_this_click = self.current_target_cps
                delay = 1.0 / cps_this_click
                elapsed = time.perf_counter() - start_click
                time.sleep(max(0.0, delay - elapsed))

            if self.config["BURST_PAUSE"] > 0: 
                time.sleep(self.config["BURST_PAUSE"])

            if self.current_clicks >= self.current_target_cps * 2:
                self.current_clicks = 0
                self.current_target_cps = self.config["CPS"] + random.uniform(-self.config["CPS_VARIANCE"], self.config["CPS_VARIANCE"])

    def start(self):
        if not self.is_active:
            self.is_active = True
            if self.click_thread is None or not self.click_thread.is_alive():
                self.click_thread = threading.Thread(target=self.click_loop, daemon=True)
                self.click_thread.start()
            print(f"[{self.config['TOGGLE_INPUT']}] Started")

    def stop(self):
        self.is_active = False
        print(f"[{self.config['TOGGLE_INPUT']}] Stopped")

    def toggle(self):
        if self.is_active:
            self.stop()
        else:
            self.start()
