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

    shutil.copytree(UNPACKED_DIR, TEMP_DIR, dirs_exist_ok=True)

    for pack in MOD_DIR.iterdir():
        if pack.is_dir() and not pack.stem.startswith('_'):
            print("adding", pack.stem)
            shutil.copytree(pack / 'assets', TEMP_DIR / 'root/assets', dirs_exist_ok=True)
    
    if SCRIPT_DIR.exists():
        print()
        print("parsing scripts...")
        print()
        inject(SCRIPT_DIR, TEMP_DIR / 'root/js/app.min.js')
    
    print()
    print("packing archive...")

    os.system(f'npm exec -- asar pack {TEMP_DIR} {ASAR_NEW_PATH}' + ' --unpack-dir "node_modules/{electron_deeplink,greenworks}"')

    shutil.rmtree(TEMP_DIR)


def inject(filepath, dest):
    contents = ""

    with open(dest, "r", encoding="utf-8") as target:
        contents = target.read()
        
    for f in filepath.iterdir():

        print("adding", f.stem)

        script = {}
        with open(f, "r") as file:
            script["regex"] = file.readline().rstrip('\n')
            script["mode"] = file.readline().rstrip('\n')
            script["data"] = file.read().rstrip('\n')

        regex = re.compile(script["regex"])
        match = regex.search(contents)

        if not match:
            print(f"failed to match {script["regex"]}!")
            continue

        if not script["mode"] in ["after", "before", "replace"]:
            print(f"unknown mode {script["mode"]}")
            continue

        if script["mode"] == "after":
            contents = contents[:match.end()] + script["data"] + contents[match.end():]
        elif script["mode"] == "before":
            contents = contents[:match.start()] + script["data"] + contents[match.start():]
        elif script["mode"] == "replace":
            contents = contents[:match.start()] + script["data"] + contents[match.end():]

    with open(dest, "w", encoding="utf-8") as target:
        target.write(contents)


if __name__ == "__main__": main()