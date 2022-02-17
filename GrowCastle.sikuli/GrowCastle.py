import time

# Auxiliary methods
seguir = True
def stop(evento):
    global seguir
    seguir = False

Env.addHotkey(Key.F1, KeyModifier.CTRL, stop)

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

def is_ready_to_battle():
    return exists("battle_button.png")


def is_inside_wave():
    return exists("wave_icon.png")


def replay():
    wait("replay_button.png")
    click("replay_button.png")
    click_if_exists("replay_type_latest_button.png")

    log("Replaying latest wave")
    wait("wave_icon.png")
    click_if_exists("speed_1x.png")

    return True


def watch_add_if_exists():
    if not click_if_exists("show_add_button.png"):
        return
    wait("add_seconds_remaining.png")
    waitVanish("add_seconds_remaining.png")

    wait("add_close_button.png")
    if not click_if_exists("add_close_button.png"):
       log_error("It was not possible to close add button")

# Program start
log("Program started, press 'Ctrl + F1' to stop it")
time.sleep(1) # TODO: change it to allow user to read the message

watch_add_if_exists()
print("success")


#while (seguir):
#    exit(0)