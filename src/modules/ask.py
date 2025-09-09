def ask_int(prompt, default):
    try:
        val = input(f"{prompt} [{default}]: ").strip()
        return int(val) if val else default
    except ValueError:
        print("⚠ Invalid input, using default.")
        return default


def ask_float(prompt, default):
    try:
        val = input(f"{prompt} [{default}]: ").strip()
        return float(val) if val else default
    except ValueError:
        print("⚠ Invalid input, using default.")
        return default


def ask_bool(prompt, default):
    val = input(f"{prompt} (y/n) [{'y' if default else 'n'}]: ").lower().strip()
    if val == "":
        return default
    return val.startswith("y")


def ask_binding():
    print("\n=== Add New Binding ===")

    toggle_input = input("Toggle key/button (e.g., q, x2) [q]: ").strip() or "q"
    while_held = ask_bool("While held?", True)
    cps = ask_int("CPS", 12)
    variance = ask_int("CPS variance", 4)
    burst_amount = ask_int("Burst amount", 1)
    burst_pause = ask_float("Burst pause (seconds)", 0.05)
    double_click_chance = ask_int("Double click chance (%)", 40)

    jitter_amount = ask_int("Jitter amount (0 = off)", 0)
    if jitter_amount > 0:
        jitter_chance = ask_int("Jitter chance (%)", 20)
        jitter_min_dur = ask_float("Jitter min duration", 0.03)
        jitter_max_dur = ask_float("Jitter max duration", 0.07)
    else:
        jitter_chance = 0
        jitter_min_dur = 0.0
        jitter_max_dur = 0.0

    is_right_click = ask_bool("Use right-click instead of left?", False)
    is_block_hitting = ask_bool("Enable block hitting?", False)

    new_binding = {
        "TOGGLE_INPUT": toggle_input,
        "WHILE_HELD": while_held,
        "CPS": cps,
        "CPS_VARIANCE": variance,
        "BURST_AMOUNT": burst_amount,
        "BURST_PAUSE": burst_pause,
        "DOUBLE_CLICK_CHANCE": double_click_chance,
        "JITTER_AMOUNT": jitter_amount,
        "JITTER_CHANCE": jitter_chance,
        "JITTER_MIN_DUR": jitter_min_dur,
        "JITTER_MAX_DUR": jitter_max_dur,
        "IS_RIGHT_CLICK": is_right_click,
        "IS_BLOCK_HITTING": is_block_hitting,
        "HIT_CPS": cps,
        "BLOCK_CPS": cps,
        "BLOCK_TO_HIT_RATIO": 0.5,
    }

    return new_binding