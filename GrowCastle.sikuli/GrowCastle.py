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

def do_exist(image):
    return exists(image) is not None

def get_replay_button_pattern():
    return Pattern("replay_button.png").similar(0.7)

def replay_or_error():
    print("replay_or_error")
    print(do_exist("replay_button.png"))
    print(exists("replay_button.png"))
    #if not do_exist("replay_button.png"):
    #   wait("replay_button.png")
    #if not do_exist("replay_button.png"):
    #    log_error("It was not possible to replay the game")

    times_searching_button = 0
    while not exists(get_replay_button_pattern()):
        times_searching_button += 1
        print("Times searching button: " + str(times_searching_button))
        wait(1)
        if times_searching_button > 20:
            log_error("It was not possible to click on replay button")

    click(get_replay_button_pattern())
    click_if_exists("replay_type_latest_button.png")


def replay_latest_wave(iteration):
    replay_or_error()
    log("Replaying latest wave (times " + str(iteration) + ")")
    wait("wave_icon.png")
    click_if_exists("speed_1x.png")

    waitVanish("wave_icon.png")
    time.sleep(4)
    #wait("replay_button.png")


def watch_add_if_exists():
    if not click_if_exists("show_add_button.png"):
        return

    wait("add_seconds_remaining.png")
    waitVanish("add_seconds_remaining.png")

    wait("add_close_button.png")
    if not click_if_exists("add_close_button.png"):
       log_error("It was not possible to close add button")


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
    watch_add_if_exists()
    time.sleep(6)
    print("sleep done")
    print(exists("replay_button.png"))

log("Program aborted")