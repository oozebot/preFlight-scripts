#/|/ Copyright (c) 2026 Your Name
#/|/
#/|/ Released under AGPLv3 or higher
#/|/
# preflight-api: 1
# modifies-gcode: yes
# firmware: any
# access: none
"""One line stating what the script does.

What it changes and when to use it. What each constant below means. What
the script does not handle, for example multi-extruder prints.
"""

import preFlight
from preFlight import MoveType, ExtrusionRole

# Every value a user must tune goes here, with its unit.
# Defaults are safe to run untuned: at 1.0 this template changes nothing.
EXTERNAL_PERIMETER_SPEED_FACTOR = 1.0  # multiplier on feedrate, 1.0 = no change


def process(gcode: preFlight.GCode):
    if EXTERNAL_PERIMETER_SPEED_FACTOR == 1.0:
        print("[process_template] factor is 1.0, nothing to do")
        return

    changed = 0
    for layer in gcode.layers:
        for move in layer.moves:
            if move.type != MoveType.Extrude:
                continue
            if move.role == ExtrusionRole.ExternalPerimeter:
                move.feedrate *= EXTERNAL_PERIMETER_SPEED_FACTOR
                move.annotation = f"process_template x{EXTERNAL_PERIMETER_SPEED_FACTOR}"
                changed += 1

    print(f"[process_template] changed {changed} external perimeter moves")
