# inject.py
# catroidvania
# dec 15 2024

# script for injecting javascript into app.min.js

import re
import shutil
import sys
from pathlib import Path


PAYLOADS_DIR = Path("js")
UNPACKED_DIR = Path("stugio_src")


def inject(filepath, dest):
    backup = dest.parent / '_app.min.js'
    contents = ""
    
    if not backup.exists():
        shutil.copy(dest, backup)
    else:
        restore(dest)

    with open(dest, "r", encoding="utf-8") as target:
        contents = target.read()
        
    for f in filepath.iterdir():

        print("injecting", f.stem, end="...")

        payload = {}
        with open(f, "r") as file:
            payload["regex"] = file.readline().rstrip('\n')
            payload["mode"] = file.readline().rstrip('\n')
            payload["data"] = file.read().rstrip('\n')

        regex = re.compile(payload["regex"])
        match = regex.search(contents)

        if not match:
            print(f"could not match {payload["regex"]}!")
        else:            
            if payload["mode"] == "inject":
                contents = contents[:match.end()] + payload["data"] + contents[match.end():]
            elif payload["mode"] == "injectbefore":
                contents = contents[:match.start()] + payload["data"] + contents[match.start():]
            elif payload["mode"] == "replace":
                contents = contents[:match.start()] + payload["data"] + contents[match.end():]

        print(" injected")

    with open(dest, "w", encoding="utf-8") as target:
        target.write(contents)

def restore(dest):
    backup = dest.parent / '_app.min.js'

    if not backup.exists():
        print("could not locate backup!")
        return
    
    shutil.copy(backup, dest)


def main():
    if len(sys.argv) > 1 and sys.argv[1] in ["r", "restore"]:
        restore(UNPACKED_DIR / 'root/js/app.min.js') 
        print("backup restored")
    elif PAYLOADS_DIR.exists():
        inject(PAYLOADS_DIR, UNPACKED_DIR / 'root/js/app.min.js')


if __name__ == "__main__": main()