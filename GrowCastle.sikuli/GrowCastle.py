import time

# Auxiliary methods
continue_execution = True
def stop(evento):
    global continue_execution
    log("Program aborted")
    continue_execution = False


def log(message):
    print("[INFO] " + message)


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
    # This method return found pattern index
    seconds_searching_pattern = 0
    while True:
        pattern_index = get_existing_pattern_index(patterns)
        if pattern_index is not None:
            return pattern_index

        seconds_searching_pattern += 1
        wait(1)
        if max_seconds is None and seconds_searching_pattern > 45:
            log_error("It was not possible to click on any pattern from '" + str(patterns) + "'")
        elif max_seconds is not None and seconds_searching_pattern > max_seconds:
            return None


def force_wait_pattern(pattern):
    return force_wait_any_pattern([pattern])


def force_wait_main_page():
    force_wait_pattern(get_replay_button_pattern())
    time.sleep(1)


def replay_latest_wave(iteration):
    click(get_replay_button_pattern())
    click_if_exists("replay_type_latest_button.png")
    log("Replaying latest wave (times " + str(iteration) + ")")
    wait("wave_icon.png")
    click_if_exists("speed_1x.png")
    waitVanish("wave_icon.png")


def force_add_close(attempt):
    close_add_button_patterns = [get_pattern("add_close_button_white_background.png", 0.9), get_pattern("add_close_button_black_background.png", 0.9)]
    found_pattern_index = force_wait_any_pattern(close_add_button_patterns)
    print("found_pattern_index" + str(found_pattern_index))
    close_button = close_add_button_patterns[found_pattern_index]
    if click_if_exists(close_button):
        if not is_inside_main_page():
            time.sleep(1)
            if is_inside_main_page:
                return
            log("Add close button needs to be clicked clicked again " + str(attempt) + " times")
            if attempt > 30:
                log_error("It was not possible to close the add after 30 attempts")
            force_add_close(attempt + 1)
    else:
        log_error("It was not possible to close the add")


def watch_add_if_exists():
    if not click_if_exists("show_add_button.png"):
        return

    add_seconds_pattern = get_pattern("add_in_progress_seconds_remaining.png", 0.8)
    waitVanish(add_seconds_pattern)

    print("waiting google play icon search")
    force_wait_any_pattern_or_max_seconds(["add_finished_google_play_icon.png", "add_finished_reward_granted.png"], 45)
    force_add_close(1)


# Program start
Env.addHotkey(Key.F1, KeyModifier.CTRL, stop)
log("Program started, press 'Ctrl + F1' to stop it")
time.sleep(1)

if not is_inside_main_page():
    log_error("Simulator must be inside the game (battle button must be available)")

times = 0
while continue_execution:
    times += 1
    replay_latest_wave(times)
    force_wait_main_page()
    watch_add_if_exists()

log("Program aborted")