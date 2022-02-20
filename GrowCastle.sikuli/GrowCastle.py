import time

# Configuration
show_logs = True
battle_next_waves = True
watch_advertisements = True
spend_diamonds = False  # There is a limit in the amount of diamonds to hold. Prevent waste of diamonds using them
waves_to_use_diamonds = 20


# Auxiliary methods
def stop(event):
    log("Program aborted")
    exit(0)


def log(message):
    if show_logs:
        print("[INFO] " + message)


def log_warning(message):
    if show_logs:
        print("[WARNING] " + message)


def log_error(message):
    print("[ERROR] " + message)
    exit(1)


def click_if_exists(image):
    if exists(image):
        click(image)
        return True
    return False


def is_inside_main_page():
    return exists("battle_button.png")


def get_replay_button_pattern():
    return pattern("replay_button.png", 0.8)


def get_castle_canon_ball_pattern():
    return pattern("castle_canon_ball.png", 0.9)


def pattern(image, similarity):
    return Pattern(image).similar(similarity)


def get_existing_pattern_index(patterns):
    for count, current_pattern in enumerate(patterns):
        if exists(current_pattern):
            return count

    return None


def force_wait_any_pattern(patterns):
    return force_wait_any_pattern_or_max_seconds(patterns, None)


def force_wait_any_pattern_or_max_seconds(patterns, max_seconds):
    log("Method force_wait_any_pattern_or_max_seconds(" + str(patterns) + ", " + str(max_seconds) + ")")
    # This method return found pattern index
    seconds_searching_pattern = 0
    while True:
        pattern_index = get_existing_pattern_index(patterns)
        if pattern_index is not None:
            return pattern_index

        seconds_searching_pattern += 1
        time.sleep(1)
        if max_seconds is None and seconds_searching_pattern > 45:
            log_error("It was not possible to click on any pattern from '" + str(patterns) + "'")
        elif max_seconds is not None and seconds_searching_pattern >= max_seconds:
            return None


def force_wait_pattern(pattern):
    return force_wait_any_pattern([pattern])


def force_wait_main_page():
    log("Method force_wait_main_page")
    force_wait_pattern(get_replay_button_pattern())
    time.sleep(1)


def battle_next_wave(iteration):
    log("Battle next wave (times " + str(iteration) + ")")
    click(pattern("battle_button.png", 0.8))
    return wait_wave_to_finish()


def replay_latest_wave(iteration):
    log("Replaying latest wave (times " + str(iteration) + ")")
    click(get_replay_button_pattern())
    click_if_exists("replay_type_latest_button.png")
    return wait_wave_to_finish()


def wait_wave_to_finish():
    # Returns True (Victory) or False (Defeat)
    log("Method wait_wave_to_finish")
    wait("wave_icon.png")
    click_if_exists("speed_1x.png")

    max_wave_seconds = 600
    while max_wave_seconds > 0 and exists(pattern("wave_icon.png", 0.9)):
        max_wave_seconds -= 1
        click_if_exists("treasure.png")
        time.sleep(1)
    if max_wave_seconds <= 0:
        log_error("It was not possible to wait wave to finish")


def detect_add_seconds():
    log("Method wait_add_to_finish")
    print(exists(pattern("img/adds/add_10_secs.png", 0.5)))
    print(exists(pattern("img/adds/add_20_secs.png", 0.5)))
    if exists(pattern("img/adds/add_10_secs.png", 0.97)):
        log("Detected add 10 seconds")
        return 12
    elif exists(pattern("img/adds/add_20_secs.png", 0.97)):
        log("Detected add 20 seconds")
        return 22

    return 32


def wait_add_to_finish():
    log("Method wait_add_to_finish")
    waiting_seconds = detect_add_seconds()
    time.sleep(waiting_seconds)


def close_add():
    log("Method close_add")
    close_add_button_patterns = [pattern("img/adds/add_close_button_white_background.png", 0.9),
                                 pattern("img/adds/add_close_button_black_background.png", 0.9),
                                 pattern("img/adds/add_close_button_grey_background.png", 0.9)]
    found_pattern_index = force_wait_any_pattern(close_add_button_patterns)
    close_button = close_add_button_patterns[found_pattern_index]
    if click_if_exists(close_button):
        if not is_inside_main_page():
            time.sleep(1)
            if not is_inside_main_page:
                log_error("Close button for add was not clicked successfully")
    else:
        log_error("It was not possible to close the add")


def watch_add_if_exists():
    log("Method watch_add_if_exists")
    if not click_if_exists("show_add_button.png"):
        return

    wait_add_to_finish()
    close_add()


def inside_canon_screen():
    return exists(get_castle_canon_ball_pattern())


def use_diamonds(quantity):
    # Precondition: at least 'quantity' diamonds must be available
    if quantity <= 0:
        return

    log("Using " + str(quantity) + "diamonds")
    if not inside_canon_screen():
        inside_canon = click_if_exists(pattern("castle_show_canons.png", 0.9))
        if not inside_canon:
            log_warning("It was not possible to use diamonds. Can not enter canons screen")
            return

    inside_canon_upgrades = click_if_exists(get_castle_canon_ball_pattern())
    if not inside_canon_upgrades:
        log_warning("It was not possible to use diamonds. Can not enter canons upgrades screen")
        return

    for i in range(quantity):
        click(pattern("castle_canon_level_up_button.png", 0.9))

    type(Key.ESC)  # Close canon upgrade screen
    type(Key.ESC)  # CLose canons screen


# Program start
Env.addHotkey(Key.F1, KeyModifier.CTRL, stop)
log("Program started, press 'Ctrl + F1' to stop it")
time.sleep(1.5)

if not is_inside_main_page():
    log_error("Simulator must be inside the game (battle button must be available)")

times = 0
while True:
    times += 1
    if battle_next_waves:
        battle_next_wave(times)
    else:
        replay_latest_wave(times)

    force_wait_main_page()

    if watch_advertisements:
        watch_add_if_exists()

    if spend_diamonds and (times % waves_to_use_diamonds) == 0 and times > 0:
        use_diamonds(waves_to_use_diamonds)
