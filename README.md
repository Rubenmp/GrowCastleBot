# Grow Castle bot
This is a bot for the game [Grow Castle](https://play.google.com/store/apps/details?id=com.raongames.growcastle&hl=en&gl=US).

It uses phone mirroring and image recognition to interact with the game.


## Requirements
- Install an emulator to mirror your phone into your computer
    - For this demo, [scrcpy](https://github.com/Genymobile/scrcpy) is used inside Ubuntu 20.04.3 LTS.
    [USB debugging](https://www.youtube.com/watch?v=Ucs34BkfPB0&t=25s) must be enabled in the phone. Maybe ['connect as MTP' phone setting is also required](https://stackoverflow.com/questions/28704636/insufficient-permissions-for-device-in-android-studio-workspace-running-in-opens).
- Install Sikulix (used for image recognition and interface interactions)
- Basic knowledge about Python scripting language


## Execution
- Run the phone emulator
```console
$ scrcpy
```

- Create alias for sikulix jar
```console
$ alias RunGrowCastleBot='java -jar sikulixide-2.0.5.jar -r GrowCastle.sikuli'
```

- Run the program
```console
$ RunGrowCastleBot
```

Or directly copy Sikulix jar in the root folder and run
```console
$ java -jar sikulixide-2.0.5.jar -r GrowCastle.sikuli/
```
