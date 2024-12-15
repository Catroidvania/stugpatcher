# stugpatcher

a modding script for stug io

this is an unofficial python script to help speed up patching assets into the game

use at your own risk

# dependancies

* [npm/nodejs](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
* [electron asar](https://github.com/electron/asar), install with npm
* [python >=3.12.6](https://www.python.org/downloads/)

calling node scripts through the command line is pretty gross but there arent any working asar handling libraries for python atm :/

# usage

1. download and extract the repository contents
2. locate your `app.asar` in steam > gear icon > manage > browse local files > resources
3. copy `app.asar` and `app.asar.unpacked` to the folder with `patcher.py`
4. add asset packs to `custom` folder (you might need to create this if it isnt there)
5. run `patcher.py`, it might take a minute or two to extract
6. copy `app_modded.asar` back to the steam files and rename to replace the orignal `app.asar`

asset pack name starting with an underscore will be ignored

running `clean.bat` deletes `app_modded.asar`, `app_modded.asar.unpacked`, and `stugio_src`

# creating asset packs

assets packs are directories mimicing the contents of `stugio_src\root\assets` containing the files you want to replace

the structure might look something like

```
pack_name
└── assets
    ├── emotes
    │   ├── emote_heart.webp
    │   └── emote_hello.webp
    ├── vehicles
    │   └── light_tank
    │       └── light_tank_thumbnail.webp
    ├── crosshair.webp
    └── kill.ogg
```