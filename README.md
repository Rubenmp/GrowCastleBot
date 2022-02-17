# Grow Castle bot
This is a bot for the game [Grow Castle](https://play.google.com/store/apps/details?id=com.raongames.growcastle&hl=en&gl=US).

![Grow Castle Bot Demo](./GrowCastleBotDemo.gif)

It uses phone mirroring and images recognition to interact with the game, **replaying the last wave indefinitely**.


## Requirements
- Install an emulator to mirror your phone into your computer
    - For this demo, [scrcpy](https://github.com/Genymobile/scrcpy) is used inside Ubuntu 20.04.3 LTS.
    [USB debugging](https://www.youtube.com/watch?v=Ucs34BkfPB0&t=25s) must be enabled in the phone. Maybe ['connect as MTP' phone setting is also required](https://stackoverflow.com/questions/28704636/insufficient-permissions-for-device-in-android-studio-workspace-running-in-opens).
- [Install Sikulix](http://sikulix.com/quickstart/) (used for image recognition and interface interactions)
- (Optional) Basic knowledge about [Python](https://www.python.org/) scripting language


## Execution
- Run the phone emulator
```console
$ scrcpy
```

- Create alias and execute the bot
```console
$ alias RunGrowCastleBot='java -jar SIKULIX_JAR_DIR/sikulixide-2.0.5.jar -r GrowCastle.sikuli'
$ RunGrowCastleBot
```


## Improvements
- Detect victory/defeat for each wave. Use this information to dynamically battle the next waves, not just replay the last one.
- Click on treasures ("treasure.png") in the middle of the waves, not just wait until the end.
