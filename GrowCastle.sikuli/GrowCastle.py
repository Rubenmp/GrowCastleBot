import time

# Configuration


# Auxiliary methods
seguir = True
def stop(evento):
    global seguir
    seguir = False

Env.addHotkey(Key.F1, KeyModifier.CTRL, stop)

def log(message):
    print("[INFO] " + message)


def is_ready_to_battle():
    return exists("battle_button.png")


def is_inside_wave():
    return exists("wave_icon.png")


def replay():
    wait("replay_button.png")
    click("replay_button.png")
    if exists("replay_type_latest_button.png"):
        click("replay_type_latest_button.png")

    log("Replaying latest wave")
    return True


# Program start
log("Program started, press 'Ctrl + F1' to stop it")
time.sleep(1) # TODO: change it to allow user to read the message

replay()


#while (seguir):
#    exit(0)