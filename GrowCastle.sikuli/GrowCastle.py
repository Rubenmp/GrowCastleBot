import time

# Auxiliary methods
continue_execution = True
def stop(evento):
    global continue_execution
    log("Program aborted")
    continue_execution = False


def accelerate_sikulix():
    Settings.MoveMouseDelay = 0
    Settings.DelayBeforeMouseDown = 0


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


def is_inside_game():
    return exists("battle_button.png")


def get_replay_button_pattern():
    return get_pattern("replay_button.png", 0.8)


def get_pattern(image, similarity):
    return Pattern(image).similar(similarity)


def force_wait_pattern(pattern):
    times_searching_button = 0
    while not exists(pattern):
        times_searching_button += 1
        wait(1)
        if times_searching_button > 20:
            log_error("It was not possible to click on pattern '" + str(pattern) + "'")
    time.sleep(1)


def replay_latest_wave(iteration):
    click(get_replay_button_pattern())
    click_if_exists("replay_type_latest_button.png")
    log("Replaying latest wave (times " + str(iteration) + ")")
    wait("wave_icon.png")
    click_if_exists("speed_1x.png")

    waitVanish("wave_icon.png")
    time.sleep(4)


def watch_add_if_exists():
    if not click_if_exists("show_add_button.png"):
        return

    add_seconds_pattern = get_pattern("add_seconds_remaining.png", 0.8)
    waitVanish(add_seconds_pattern)

    add_close_pattern = get_pattern("add_close_button.png", 0.9)
    force_wait_pattern(add_close_pattern)
    if not click_if_exists("add_close_button.png"):
       log_error("It was not possible to close the add")


# Program start
Env.addHotkey(Key.F1, KeyModifier.CTRL, stop)
log("Program started, press 'Ctrl + F1' to stop it")
#time.sleep(4)

if not is_inside_game():
    log_error("Simulator must be inside the game (battle button must be available)")


times = 0
while continue_execution:
    times += 1
    replay_latest_wave(times)
    force_wait_pattern(get_replay_button_pattern())
    watch_add_if_exists()
    time.sleep(6)

log("Program aborted")