#/|/ Copyright (c) 2026 Your Name
#/|/
#/|/ Released under AGPLv3 or higher
#/|/
# preflight-api: 1
# modifies-gcode: no
# firmware: any
# access: files
"""One line stating where the G-code goes.

What the script does with the file, what it connects to, and what each
constant below means.
"""

import os
import preFlight

# Every value a user must set goes here.
# An unconfigured script refuses to run instead of guessing: this template
# stops until OUTPUT_FOLDER is set.
OUTPUT_FOLDER = ""  # folder to save into, e.g. "D:/gcode" or "/mnt/printer"


def export(gcode: preFlight.ExportGCode):
    if not OUTPUT_FOLDER:
        raise RuntimeError("[export_template] OUTPUT_FOLDER is not set: edit the script to choose a destination")

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    path = os.path.join(OUTPUT_FOLDER, gcode.filename)

    # newline="" keeps the line ends as they are. Without it, Windows writes CR LF.
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.writelines(gcode.data)

    print(f"[export_template] wrote {path}")
