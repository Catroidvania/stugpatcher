# patcher.py
# catroidvania
# dec 15 2024

# script for moddding the steam version of stug.io

from pathlib import Path
import os
import re
import shutil


MOD_DIR = Path("packs")
SCRIPT_DIR = Path("scripts")
UNPACKED_DIR = Path("stugio_src")
TEMP_DIR = Path("temp_")
ASAR_PATH = Path("app.asar")
ASAR_NEW_PATH = Path("app_modded.asar")
APP_MIN_JS_PATH = TEMP_DIR / 'root/js/app.min.js'
APP_MIN_JS_FILE = {"contents": ""}


def main():

    if not ASAR_PATH.exists():
        raise FileNotFoundError("could not find app.asar!")

    if not MOD_DIR.exists():
        MOD_DIR.mkdir()
    
    if not TEMP_DIR.exists():
        TEMP_DIR.mkdir()

    # no working asar libraries for python :/ too lazy to write one myself rn so this will have to do
    if not UNPACKED_DIR.exists():
        print("unpacking app.asar...")
        os.system(f"npm exec -- asar extract {ASAR_PATH} {UNPACKED_DIR}")
        print()

    # create a temp dir to retain an unmodified copy of the source
    # this stops code injects repeatedly matching with previous changes
    shutil.copytree(UNPACKED_DIR, TEMP_DIR, dirs_exist_ok=True)

    with open(APP_MIN_JS_PATH, "r", encoding="utf-8") as file:
        APP_MIN_JS_FILE["contents"] = file.read()

    for pack in MOD_DIR.iterdir():
        if pack.is_dir() and not pack.stem.startswith('_'):
            print("adding", pack.stem)
            shutil.copytree(pack / 'assets', TEMP_DIR / 'root/assets', dirs_exist_ok=True)

            # automatically inject contents of tmx files for adding research trees and vehicles
            for file in (pack / 'assets').iterdir():
                if file.suffix == ".tmx":
                    print("  +", file.stem)
                    add_research_tree_data(file, APP_MIN_JS_PATH)
            
            if (pack / 'assets/vehicles').exists():
                for vehicle in (pack / 'assets/vehicles').iterdir():    # there has got to be a nicer way to do this
                    if vehicle.is_dir():
                        for file in vehicle.iterdir():
                            if file.suffix == ".tmx":
                                print("  +", file.stem)
                                add_vehicle_data(file, APP_MIN_JS_PATH)

    # load scripts
    if SCRIPT_DIR.exists():
        print()
        print("parsing scripts...")
        print()
        load_scripts(SCRIPT_DIR, TEMP_DIR / 'root/js/app.min.js')

    with open(APP_MIN_JS_PATH, "w", encoding="utf-8") as file:
        file.write(APP_MIN_JS_FILE["contents"])
    
    print()
    print("packing archive...")

    os.system(f'npm exec -- asar pack {TEMP_DIR} {ASAR_NEW_PATH}' + ' --unpack-dir "node_modules/{electron_deeplink,greenworks}"')

    shutil.rmtree(TEMP_DIR)


# injects into the js object that loads vehicle data
def add_vehicle_data(tmxpath, dest):
    data = ""
    with open(tmxpath, "r", encoding="utf-8") as file:
        data = file.read().replace('\n','')

    fn_regex = re.compile(f"{tmxpath.stem}:A\\('[^']*'\\)")
    fn_exists = fn_regex.search(APP_MIN_JS_FILE["contents"])

    if fn_exists:
        load_script(dest, f"{tmxpath.stem}:A\\('[^']*'\\)", "replace", f"{tmxpath.stem}:A('{data}')")
    else:
        load_script(dest, "light_tank:A\\(", "before", f"{tmxpath.stem}:A('{data}'),")


# modifies code to expose the unused research tabs and injects the tab data
def add_research_tree_data(tmxpath, dest):
    data = ""
    with open(tmxpath, "r", encoding="utf-8") as file:
        data = file.read().replace('\n','')

    fn_regex = re.compile(f"T\\.{tmxpath.stem}=")
    fn_exists = fn_regex.search(APP_MIN_JS_FILE["contents"])

    if fn_exists:
        load_script(dest, f"T\\.{tmxpath.stem}='[^']*'", "replace", f"T.{tmxpath.stem}='{data}'")
    else:
        tabname = tmxpath.stem.split("_")
        tabname.insert(2, "tab")
        tabnamestr = "-".join(tabname)

        load_script(dest, '\\{"' + tabnamestr + '":!0\\},disabled:!0\\}', "replace", '{"' + tabnamestr + '":!0}}')
        load_script(dest, ';for\\(var X=e\\("\\./data/vehicle_list"\\),J=0;J<X\\.length;J\\+\\+\\)', "before", f',K("{tmxpath.stem}")')
        load_script(dest, ";for\\(var I=\\{bruh:A\\(", "before", f",T.{tmxpath.stem}='{data}'")


# the old bulk injector
def load_scripts(filepath, dest):

    contents = APP_MIN_JS_FILE["contents"]
        
    for f in filepath.iterdir():

        print("adding", f.stem)

        script = {}
        with open(f, "r") as file:
            script["regex"] = file.readline().rstrip('\n')
            script["mode"] = file.readline().rstrip('\n')
            script["data"] = file.read().rstrip('\n')

        regex = re.compile(script["regex"])
        match = regex.search(APP_MIN_JS_FILE["contents"])

        if not match:
            print(f"failed to match {script["regex"]}")
            continue

        if not script["mode"] in ["after", "before", "replace"]:
            print(f"unknown mode {script["mode"]}")
            continue

        if script["mode"] == "after":
            APP_MIN_JS_FILE["contents"] = contents[:match.end()] + script["data"] + contents[match.end():]
        elif script["mode"] == "before":
            APP_MIN_JS_FILE["contents"] = contents[:match.start()] + script["data"] + contents[match.start():]
        elif script["mode"] == "replace":
            APP_MIN_JS_FILE["contents"] = contents[:match.start()] + script["data"] + contents[match.end():]


# inject one time
def load_script(dest, rgx, mode, data):

    contents = APP_MIN_JS_FILE["contents"]

    regex = re.compile(rgx)
    match = regex.search(APP_MIN_JS_FILE["contents"])

    if not match:
        print(f"failed to match {rgx}")
        return

    if not mode in ["after", "before", "replace"]:
        print(f"unknown mode {mode}")
        return
    
    #print(match)
    #print(contents[match.start():match.start()+10], "...", contents[match.end()-10:match.end()])

    if mode == "after":
        APP_MIN_JS_FILE["contents"] = contents[:match.end()] + data + contents[match.end():]
    elif mode == "before":
        APP_MIN_JS_FILE["contents"] = contents[:match.start()] + data + contents[match.start():]
    elif mode == "replace":
        APP_MIN_JS_FILE["contents"] = contents[:match.start()] + data + contents[match.end():]


if __name__ == "__main__": main()