import time

# Configuration
show_logs = True

# Auxiliary methods
continue_execution = True


def stop(event):
    global continue_execution
    log("Program aborted")
    continue_execution = False
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
        elif max_seconds is not None and seconds_searching_pattern > max_seconds:
            return None


def force_wait_pattern(pattern):
    return force_wait_any_pattern([pattern])


def force_wait_main_page():
    log("Method force_wait_main_page")
    force_wait_pattern(get_replay_button_pattern())
    time.sleep(1)


def battle_next_wave():
    log("Method battle_next_wave")
    click(get_pattern("battle_button.png", 0.8))
    click_if_exists("replay_type_latest_button.png")
    return wait_wave_to_finish()


def replay_latest_wave(iteration):
    click(get_replay_button_pattern())
    click_if_exists("replay_type_latest_button.png")
    log("Replaying latest wave (times " + str(iteration) + ")")
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

    battle_result_patterns = [get_pattern("battle_end_victory.png", 0.9)]
    pattern_index = force_wait_any_pattern_or_max_seconds(battle_result_patterns)
    if pattern_index is None:
        log_warning("It was not possible to determine wave result, assuming defeat.")
        return False

    return pattern_index == 1


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
    force_wait_any_pattern_or_max_seconds([get_pattern("add_finished_reward_granted.png", 0.8)], 3)

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


# Program start
Env.addHotkey(Key.F1, KeyModifier.CTRL, stop)
log("Program started, press 'Ctrl + F1' to stop it")
time.sleep(4)

if not is_inside_main_page():
    log_error("Simulator must be inside the game (battle button must be available)")

times = 0
while continue_execution:
    times += 1
    replay_latest_wave(times)
    force_wait_main_page()
    watch_add_if_exists()
    print("watch_add_if_exists")

log("Program finished")
