# patcher.py
# catroidvania
# dec 15 2024

# script for moddding the steam versoin of stug.io

from pathlib import Path
import os
import shutil


MOD_DIR = Path("custom")
UNPACKED_DIR = Path("stugio_src")
ASAR_PATH = Path("app.asar")
ASAR_NEW_PATH = Path("app_modded.asar")


def main():

    if not ASAR_PATH.exists():
        raise FileNotFoundError("Could not find app.asar!")

    if not MOD_DIR.exists():
        MOD_DIR.mkdir()

    # no working asar libraries for python :/
    if not UNPACKED_DIR.exists():
        os.system(f"npm exec -- asar extract {ASAR_PATH} {UNPACKED_DIR}")

    for pack in MOD_DIR.iterdir():
        if pack.is_dir() and not pack.stem.startswith('_'):
            print("adding", pack.stem)
            shutil.copytree(pack / 'assets', UNPACKED_DIR / 'root/assets', dirs_exist_ok=True)

    os.system(f'npm exec -- asar pack {UNPACKED_DIR} {ASAR_NEW_PATH}' + ' --unpack-dir "node_modules/{electron_deeplink,greenworks}"')

    print()
    print("packed")

if __name__ == "__main__": main()