#/|/ Copyright (c) preFlight 2025+ oozeBot, LLC
#/|/
#/|/ Released under AGPLv3 or higher
#/|/
"""
Save to Folder - preFlight Export to Script sample

Saves G-code to a configurable output folder. Useful for network shares,
NAS drives, SD card readers, or any mounted path.
"""
import os

# ---- Configuration ----
OUTPUT_FOLDER = ""  # e.g. "D:/gcode", "//NAS/prints", "/mnt/printer"
# -----------------------


def export(gcode):
    if not OUTPUT_FOLDER:
        raise RuntimeError("OUTPUT_FOLDER not configured - edit this script to set a destination path")

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    path = os.path.join(OUTPUT_FOLDER, gcode.filename)

    # newline='' writes the lines as they are; without it Windows turns every line end into CR LF
    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.writelines(gcode.data)
