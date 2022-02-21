# Grow Castle bot
Bot for the game [Grow Castle](https://play.google.com/store/apps/details?id=com.raongames.growcastle&hl=en&gl=US).
It uses phone mirroring with image recognition to interact with the game. The default behaviour is to **replay the last wave indefinitely**.

![Grow Castle Bot Demo](./demo/Demo.gif)


## Features
Most of the features can be customized with configuration variables in file [*GrowCastle.py*](./GrowCastle.sikuli/GrowCastle.py).
- Waves
    - Infinite waves, selection behaviour using the variable *waves_selection_pattern*, possible values:
        - REPLAY: always replay the last wave
        - BATTLE: continue with the next waves
        - MIXED: 1/10 combination of both scenarios (one BATTLE every 10 rounds, the other 9 waves will be REPLAY)
    - Game speed will be increased automatically if possible.
    - Click on the treasures found in the waves.
- Watch advertisements depending on variable *watch_advertisements* (default True).
- Update features
    - Coins: upgrade castle. It depends on variable *upgrade_castle_periodically*
    - Diamonds: upgrade castle canons. It depends on variable *spend_diamonds_on_canons* (default True). If the variable is False it could potentially lose diamonds due to the amount limit.


## Requirements
- Install an emulator to mirror your phone into your computer.
    - Emulator [scrcpy](https://github.com/Genymobile/scrcpy) was used inside Ubuntu 20.04.3 LTS operating system.
    [USB debugging](https://www.youtube.com/watch?v=Ucs34BkfPB0&t=25s) must be enabled in the phone. Probably ['connect as MTP' phone setting](https://stackoverflow.com/questions/28704636/insufficient-permissions-for-device-in-android-studio-workspace-running-in-opens) will also be required.
- [Install Sikulix](http://sikulix.com/quickstart/), used for image recognition and interface interactions.
- (Optional) Basic knowledge about [Python](https://www.python.org/) scripting language if you want to modify the behaviour.


## Execution
Run the phone emulator on your computer
```console
$ scrcpy
```

Open a terminal in the root project folder and execute the bot
```console
$ java -jar SIKULIX_JAR_DIR/sikulixide-2.0.5.jar -r GrowCastle.sikuli
```

(Optional) In the demo video an alias *RunGrowCastleBot* was created and executed.
```console
$ alias RunGrowCastleBot='java -jar SIKULIX_JAR_DIR/sikulixide-2.0.5.jar -r GrowCastle.sikuli'
$ RunGrowCastleBot
```

## Improvements
- Detect wave result (Victory/Defeat)
    - It would allow to battle the next wave or replay depending on previous results (or replay easier waves if the last wave failed, although is theoretically not possible when played automatically).
    - Attempt done, Sikulix is not fast enough to detect the "Victory" logo that lasts 0.5 seconds. It's possible to detect it using the level (lv) icon shown on the main screen. Taking snapshots ([stackoverflow](https://stackoverflow.com/questions/16745722/whats-the-command-to-take-a-picture-in-sikuli), [docs](http://doc.sikuli.org/screen.html#capturing)) before and after the wave would allow images comparison, detecting if the level changed (Victory) or not (Defeat) using a similarity threshold.
