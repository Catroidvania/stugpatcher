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
    │   └── my_tank
    │       ├── my_tank.tmx
    │       └── my_tank_hull.webp
    ├── research_tree_japan.tmx
    ├── crosshair.webp
    └── kill.ogg
```

also see `example_pack`

### sidenotes

* the contents of each pack are copied over the original game files
* packs are copied in succession so if a file is replaced in two packs, itll end up as whichever was added last
* asset packs with names starting with an underscore will be ignored

# adding custom vehicles

vehicle and research tree `.tmx` files are automatically injected into `app.min.js`

this is a pretty jank process so be careful about some things

### some things

* the vehicles folder and tmx file should have the same name
* you can use [Tiled](https://www.mapeditor.org/) to edit tmx files
    * if you want to edit the vehicle properties go to the toolbar > Map > Map Properties
    * remember to move the object and not just the image, otherwise turrets and wheels will rotate incorrectly
* because regex is used to find where to put the code, the vehicle folder and tmx names should only contain letters and underscores
    * the display name of the vehicle is a property in the vehicle tmx file
* replacing an existing vehicles tmx changes the stats in test drive but will have no effect in multiplayer
* do not click resaerch on custom vehicles it will freeze your game
* you need to make a custom research tree to access your vehicle, click on one of the ? tabs to access it
* the valid research trees are: `research_tree_britain.tmx`, `research_tree_france.tmx`, and `research_tree_japan.tmx`
    * these are the three currently unused trees that exist in the code but have disabled tabs and no associated data
    * if you try to create a tree that isnt one of those three it wont be accessible
* trees in other packs will overwrite previous ones so keep that in mind
* you can modify existing research trees but this has a very high chance of preventing your game from starting
    * it seems to have to do adding vehicles you dont have fully researched, such as custom vehicles