import os
import pickle
from modules.setup import setup_inputs
from modules.ask import ask_binding

CONFIG_DIR = "./config"
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.pickle")

# ==============================
# Default config (used for reset)
# ==============================
DEFAULT_BINDINGS = [
    {
        "TOGGLE_INPUT": "x2",
        "WHILE_HELD": True,
        "CPS": 20,
        "CPS_VARIANCE": 7,
        "BURST_AMOUNT": 2,
        "BURST_PAUSE": 0.1,
        "DOUBLE_CLICK_CHANCE": 85,
        "JITTER_AMOUNT": 0,
        "JITTER_CHANCE": 50,
        "JITTER_MIN_DUR": 0.05,
        "JITTER_MAX_DUR": 0.1,
        "IS_RIGHT_CLICK": False,
        "IS_BLOCK_HITTING": True,
        "HIT_CPS": 20,
        "BLOCK_CPS": 20,
        "BLOCK_TO_HIT_RATIO": 0.4,
    }
]

# ==============================
# Helper functions
# ==============================
def ensure_config_dir():
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

def load_config():
    ensure_config_dir()
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "rb") as f:
            return pickle.load(f)
    return DEFAULT_BINDINGS.copy()

def save_config(bindings):
    ensure_config_dir()
    with open(CONFIG_FILE, "wb") as f:
        pickle.dump(bindings, f)
    print("💾 Config auto-saved.")

def add_binding(bindings):
    new_binding = ask_binding()

    # Overwrite if same toggle key
    existing_idx = next((i for i, b in enumerate(bindings) 
                         if b["TOGGLE_INPUT"].lower() == new_binding["TOGGLE_INPUT"].lower()), None)
    if existing_idx is not None:
        old = bindings[existing_idx]
        bindings[existing_idx] = new_binding
        print(f"♻ Overwrote existing binding [{old['TOGGLE_INPUT']}]")
    else:
        bindings.append(new_binding)
        print(f"✅ Added new binding on [{new_binding['TOGGLE_INPUT']}]")

    save_config(bindings)  # auto-save

def remove_binding(bindings):
    for i, b in enumerate(bindings):
        print(f"{i+1}: {b['TOGGLE_INPUT']} (WHILE_HELD={b['WHILE_HELD']})")

    try:
        idx = int(input("Enter binding number to remove: ")) - 1
        if 0 <= idx < len(bindings):
            removed = bindings.pop(idx)
            print(f"🗑 Removed binding [{removed['TOGGLE_INPUT']}]")
            save_config(bindings)  # auto-save
        else:
            print("⚠ Invalid index.")
    except ValueError:
        print("⚠ Invalid input.")

def reset_config():
    confirm = input("⚠ Reset to default config? (y/n): ").lower()
    if confirm == "y":
        save_config(DEFAULT_BINDINGS.copy())
        print("🔄 Config reset to defaults.")
        return DEFAULT_BINDINGS.copy()
    return None

def show_bindings(bindings):
    if not bindings:
        print("⚠ No bindings configured.")
        return
    print("\n=== Current Bindings ===")
    for i, b in enumerate(bindings, start=1):
        print(f"{i}. Toggle: {b['TOGGLE_INPUT']}, While Held: {b['WHILE_HELD']}, "
              f"CPS: {b['CPS']}±{b['CPS_VARIANCE']}, Burst: {b['BURST_AMOUNT']}, "
              f"Double Click Chance: {b['DOUBLE_CLICK_CHANCE']}%, Jitter: {b['JITTER_AMOUNT']}, "
              f"Right Click: {b['IS_RIGHT_CLICK']}, Block Hitting: {b['IS_BLOCK_HITTING']}")

# ==============================
# Main Menu
# ==============================
def main():
    bindings = load_config()

    while True:
        print("\n\033[92m=== AutoClicker Config Menu ===\033[0m")
        print("\033[94m1. \033[0mAdd new binding")
        print("\033[94m2. \033[0mRemove binding")
        print("\033[94m3. \033[0mStart clicker")
        print("\033[94m4. \033[0mReset config")
        print("\033[94m5. \033[0mShow all bindings")
        print("\033[91m6. \033[0mExit")
        print("\033[93mTip: Press i+s+c at any time to return to menu\033[0m")

        choice = input("Choose option: ").strip()

        if choice == "1":
            add_binding(bindings)
        elif choice == "2":
            remove_binding(bindings)
        elif choice == "3":
            print("🚀 Starting clicker...")
            setup_inputs(bindings)
        elif choice == "4":
            new_cfg = reset_config()
            if new_cfg:
                bindings = new_cfg
        elif choice == "5":
            show_bindings(bindings)
        elif choice == "6":
            print("👋 Exiting...")
            break
        else:
            print("⚠ Invalid choice.")

if __name__ == "__main__":
    main()
