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


# Program start
log("Program started, press 'Ctrl + F1' to stop it")




#while (seguir):
#    exit(0)