import time

# Configuration
show_logs = True
battle_next_waves = False
watch_advertisements = True
use_diamonds = True  # There is a limit in the amount of diamonds to hold. Prevent waste of diamonds using them


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
    return get_pattern("replay_button.png", 0.8)


def get_castle_canon_ball_pattern():
    return get_pattern("castle_canon_ball.png", 0.9)


def get_pattern(image, similarity):
    return Pattern(image).similar(similarity)


def get_existing_pattern_index(patterns):
    for count, pattern in enumerate(patterns):
        if exists(pattern):
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
    click(get_pattern("battle_button.png", 0.8))
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
    while max_wave_seconds > 0 and exists(get_pattern("wave_icon.png", 0.9)):
        max_wave_seconds -= 1
        click_if_exists("treasure.png")
        time.sleep(1)
    if max_wave_seconds <= 0:
        log_error("It was not possible to wait wave to finish")


def is_add_in_progress():
    return exists(get_pattern("add_in_progress_second.png", 0.9)) \
           or exists(get_pattern("add_in_progress_seconds_remaining.png", 0.85)) \
           or exists(get_pattern("add_in_progress_reward_in.png", 0.9))


def force_add_close():
    log("Method force_add_close")
    max_wait = 40
    while is_add_in_progress():
        max_wait -= 1
        if max_wait <= 0:
            log_error("Waiting add to disappear")
        time.sleep(1)
    force_wait_any_pattern_or_max_seconds([get_pattern("add_finished_reward_granted.png", 0.8)], 2)

    close_add_button_patterns = [get_pattern("add_close_button_white_background.png", 0.9),
                                 get_pattern("add_close_button_black_background.png", 0.9)]
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

    force_add_close()


def inside_canon_screen():
    return exists(get_castle_canon_ball_pattern())


def use_diamonds(quantity):
    if quantity <= 0:
        return

    if not inside_canon_screen():
        inside_canon = click_if_exists(get_pattern("castle_show_canons.png", 0.9))
        if not inside_canon:
            log_warning("It was not possible to use diamonds. Can not enter canons screen")
            return

    inside_canon_upgrades = click_if_exists(get_castle_canon_ball_pattern())
    if not inside_canon_upgrades:
        log_warning("It was not possible to use diamonds. Can not enter canons upgrades screen")
        return

    for i in range(quantity):
        print(click_if_exists(get_pattern("castle_canon_level_up_button.png", 0.9)))

    type(Key.ESC)  # Close canon upgrade screen
    type(Key.ESC)  # CLose canons screen
    exit(0)


# Program start
Env.addHotkey(Key.F1, KeyModifier.CTRL, stop)
log("Program started, press 'Ctrl + F1' to stop it")
time.sleep(1.5)

if not is_inside_main_page():
    log_error("Simulator must be inside the game (battle button must be available)")

times = 0
while True:
    times += 1

    use_diamonds(10)
    exit(0)

if battle_next_waves:
    battle_next_wave(times)
else:
    replay_latest_wave(times)

force_wait_main_page()

if watch_advertisements:
    watch_add_if_exists()
