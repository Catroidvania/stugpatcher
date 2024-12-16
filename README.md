# stugpatcher

a modding script for stug io

this is an unofficial python script to help speed up patching custom assets into the game

use at your own risk

# dependancies

* [npm/nodejs](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
* [electron asar](https://github.com/electron/asar), install with npm
* [python >=3.12.6](https://www.python.org/downloads/)

calling node scripts through the command line with python is pretty gross but there arent any working asar handling libraries for python atm :/

# usage

1. download and extract the repository contents
2. locate your `app.asar` in the stugio steam page > gear icon > manage > browse local files > resources
3. copy `app.asar` and `app.asar.unpacked` to the folder with `stugpatcher.py`
4. add asset packs (see below) to the `packs` folder
5. run `python stugpatcher.py`, it might take a minute or two to extract the first time
6. copy `app_modded.asar` back to the steam files and rename to replace the orignal `app.asar`

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

### sidenotes

* the contents of each pack are copied over the original game files
* packs are copied in succession so if a file is replaced in two packs, itll end up as whichever was added last
* asset packs with names starting with an underscore will be ignored

# modifying app.min.js

the script can also inject javascript into `app.min.js` for more involved modding

## usage

1. create a `scripts` folder
2. add mod files (see below)
3. run `python stugpatcher.py`

## creating mod files

mod files are just plaintext with some information about where and what to inject

```
[regex]
[after|before|replace]
[code to inject...]
```

the first line contains a regex describing where the injection should happen
* if multiple lines would match, the injection only happens at the first match

the second line describes where the code is placed relative to the regex match
* `after` places the code after the matched string
* `before` places the code before the matched string
* `replace` replaces the matched string

the rest of the file contains the code you want to add

### sidenotes

* `stugio_src` is the unmodified contents of `app.asar`, its meant to serve as a clean base for successive patches and to save on extraction time so its not meant to be modified