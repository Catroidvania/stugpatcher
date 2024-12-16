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
2. locate your `app.asar` in stugio steam page > gear icon > manage > browse local files > resources
3. copy `app.asar` and `app.asar.unpacked` to the folder with `patcher.py`
4. add asset packs to `custom` folder (you might need to create this if it isnt there)
5. run `python patcher.py`, it might take a minute or two to extract
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

# modifying app.min.js

`injector.py` is a quick n' dirty helper script that injects javascript into `app.min.js`

this is more advanced stuff so make sure you have some idea of what youre doing

## usage

1. make sure `app.asar` has been extracted properly
2. create a `js` folder
3. add inject files (see below)
4. run `python injector.py`
5. run `python patcher.py` to repack the archive

## creating inject files

inject files are just plaintext with some information about the injection

```
[regex]
[after|before|replace]
[code to inject...]
```

the first line contains a regex describing where the injection should happen
* each regex should only match once

the second line describes where the code is placed relative to the regex match
* `after` places the code after the matched string
* `before` places the code before the matched string
* `replace` replaces the matched string

the rest of the file contains the code you want to add

### sidenotes

* the file contents are modified in sequence so beware of adding code that might match with other regexes
* a backup file called `_app.min.js` is created and used to "reset" `app.min.js`
    * the backup is restored at the start of the script to avoid unwanted repeat injections
    * you can manually restore the file with `python injector.py r`
* `injector.py` does not repack the archive. you need to run `patcher.py` for the changes to be saved
