# preFlight scripts

Python scripts for [preFlight](https://github.com/oozebot/preFlight): the samples that ship
with each release, templates for writing your own, and a place to publish scripts for other
preFlight users.

preFlight runs two kinds of script, both in its bundled Python 3.14 runtime.

**Preprocessing**: preFlight embeds a Python interpreter in the slicing pipeline, and your
script runs as a step of G-code generation. The full object structure is exposed to it:
layers, moves, feedrates, fan speeds, coordinates, extrusion roles, volumetric flow rates,
the motion planner's figures for each move, and all 400+ settings. The script iterates over
objects, not text, and what it modifies is the G-code preFlight exports. The time estimate,
the filament statistics, the M73 progress codes and the preview are computed from the
modified result. preFlight still runs post-processing scripts on the exported file, but
they are deprecated in favor of preprocessing.

Scripts attach at three levels. Print Settings, Filament Settings and Printer Settings each
have a Preprocessing tab with an ordered list of scripts, so a pressure advance script can
belong to the one filament it was calibrated for and a flow limiter to the printer whose
hotend it protects. At slice time the scripts of all three active profiles run together:
within a profile in the order listed, and across profiles in the order set in Preferences.

**Export to Script** runs when you choose that option from the export menu. The script
receives the finished G-code as a list of lines plus a suggested filename. preFlight writes
no file itself. The script is responsible for all output: save to a folder, upload over
FTPS, send to a networked printer, or all of them.

The feature pages for [preprocessing](https://preflight3d.com/features/preprocessing) and
[Export to Script](https://preflight3d.com/features/export-to-script) go deeper on both.

## Use at your own risk

> [!WARNING]
> Scripts in this repository can damage your printer, your prints and your computer.
> You run them at your own risk.

A script is a Python program with full access to your system: filesystem, network,
subprocesses. preFlight does not sandbox it. This is the same trust model as post-processing
scripts in any other slicer, and it is why preFlight asks for consent before running any
script.

A preprocessing script rewrites the G-code your printer executes. A wrong speed,
temperature, flow or acceleration value can ruin a print, damage the machine or start a
fire.

Nothing here is tuned for your machine. The sample values illustrate a technique, and
community scripts were written by other users for other printers. oozeBot reviews and runs
each community script before merging it, but cannot test it on every printer, firmware and
material, so a merged script is not a guarantee that it is safe or correct on yours.

Before printing with any script: read it, set its values for your setup, check the preview
and the exported G-code, and run a short test print first.

All scripts are provided "as is", without warranty of any kind. oozeBot and the script
authors are not liable for any damage or loss from their use. See sections 15 and 16 of
the [LICENSE](LICENSE).

## Repository layout

| Path | Contents |
|---|---|
| `preprocessor/` | `HOW_TO_USE.txt` (guide and API reference), `preFlight.py` (type stub) and `samples/`, copied from the current preFlight release |
| `preprocessor/process_template.py` | Template for a new preprocessing script |
| `preprocessor/community/` | Preprocessing scripts contributed by users, one folder each |
| `export/` | `HOW_TO_USE.txt`, `preFlight.py` and `samples/` for Export to Script, copied from the current release |
| `export/export_template.py` | Template for a new export script |
| `export/community/` | Export scripts contributed by users, one folder each |

Every script describes itself in the docstring at the top of the file. `HOW_TO_USE.txt`
is the full reference for each API. `preFlight.py` is a type stub generated from
preFlight's own bindings: place it next to your script and any editor with Python type
hint support autocompletes the API.

## Writing a script

A preprocessing script is a `.py` file that defines `process()`. This one slows the outer
walls by ten percent:

```python
import preFlight
from preFlight import MoveType, ExtrusionRole

def process(gcode: preFlight.GCode):
    for layer in gcode.layers:
        for move in layer.moves:
            if move.type == MoveType.Extrude and move.role == ExtrusionRole.ExternalPerimeter:
                move.feedrate *= 0.9
```

An export script defines `export(gcode)` and writes `gcode.data` wherever the file should
go. `export_template.py` is the shortest complete one.

## Samples

Preprocessing scripts that modify G-code:

- `pressure_advance.py`: pressure advance per extrusion role, for Marlin, Klipper and RepRapFirmware
- `adaptive_pressure_advance.py`: pressure advance computed per move from actual feedrate, volumetric flow and junction angle
- `flow_limiter.py`: caps volumetric flow per feature type to keep the hotend within its melt capacity
- `small_area_flow.py`: reduces flow and speed in small fill regions, where heat accumulates and features bulge
- `overhang_optimizer.py`: speed, fan and temperature changes on layers with overhang perimeters
- `fan_curves.py`: fan speed from a height curve with per-role overrides
- `first_layer_tuner.py`: a speed ramp across the first layer, with per-role factors
- `edge_slowdown.py`: slows moves near the bed edges, read from the bed shape
- `extrusion_multiplier.py`: flow ratio per feature type
- `accel_by_feature.py`: M204 acceleration per feature type
- `jerk_by_feature.py`: jerk or junction deviation per feature type
- `retraction_optimizer.py`: retraction length and speed scaled by the travel around it
- `multi_material_purge.py`: purge volume scaled by the color distance of each transition
- `motion_optimizer.py`: clamps feedrates a move cannot reach within its length, and annotates every move
- `temperature_tower.py`: steps the temperature every N layers, turning any model into a temperature tower

Read-only analysis:

- `print_analyzer.py`: time, filament and move counts by feature type, slow layers, retraction counts
- `layer_summary.py`: walks the raw text layer by layer and adds a summary comment to each
- `numpy_analysis.py`: per-layer statistics with numpy (requires `pip install numpy`)

Reference:

- `m73_progress.py`: M73 progress insertion as a script. preFlight does this natively; the sample exists to show the technique
- `api_test.py`: exercises every API binding and prints a PASS/FAIL report

Export:

- `save_to_folder.py`: writes to a configured folder
- `ftps_upload.py`: uploads over FTPS (implicit TLS, port 990) directly from memory
- `save_and_upload.py`: both

## Using a script

1. Download the `.py` file (open it on GitHub and use Raw, or clone the repository). Keep
   it outside the preFlight install folder. Your profile stores the path to the script,
   and preFlight ships self-contained, so a script inside the install folder does not
   survive an update.
2. Open the script in a text editor. Any values it needs from you are listed near the top
   as named settings, for example `MAX_FLOW = 15.0` or `TEMPS = [220, 215, 210, 205, 200,
   195]`. They are the author's numbers, for the author's printer and filament. Change any
   that apply to yours and save the file. Some scripts have none.
3. If the header has a `requires` line, install those packages: Preferences >
   Preprocessing > Open Python Console, then `pip install` the package. Only packages
   with a prebuilt wheel install; the bundled runtime has no compiler.
4. Add the script in preFlight. The first time, a security warning explains what scripts
   can do and asks for consent.
   - Preprocessing: Print, Filament or Printer Settings > Preprocessing tab > Enable
     preprocessing > Add Script. Choose the profile the script belongs with, since it
     follows that profile when you switch presets.
   - Export: Print Settings > Output options > Export to Script. After slicing, Export to
     Script appears in the export menu.
5. Slice, then check the preview and the exported G-code. A script that fails does not
   abort the slice. preFlight reports the error as a notification and produces the G-code
   without that script's changes, so read the notifications before you print.
6. Run a short test print before trusting the script on a long one.

A script's `print()` lines and its error messages go to the terminal preFlight was started
from, so start it from one. On Windows, open a terminal in the preFlight folder and run
`preFlight-console.exe`. Double-clicking it runs preFlight without showing the output. On
Linux and macOS, run the preFlight executable from a terminal. To keep a log while you
slice, redirect the output.

Windows:

```
preFlight-console.exe > debug.txt 2>&1
```

Linux, AppImage:

```
./preFlight-<version>-linux-x86_64.AppImage > debug.txt 2>&1
```

Raspberry Pi, `.deb` package:

```
preflight > debug.txt 2>&1
```

macOS:

```
/Applications/preFlight.app/Contents/MacOS/preFlight > debug.txt 2>&1
```

Pull requests with scripts come here. Questions about scripting go to the main
repository's [Discussions](https://github.com/oozebot/preFlight/discussions), and
problems, including one with a script from this repository, to its
[Issues](https://github.com/oozebot/preFlight/issues).

## Contributing a script

Submit a pull request with one `.py` file in a folder of its own:

```
preprocessor/community/<script_name>/<script_name>.py
export/community/<script_name>/<script_name>.py
```

Start from `process_template.py` or `export_template.py`. The templates show the header,
the docstring and where the tunable constants go.

The file name is the script's identity. Use lowercase letters, digits and underscores, and
choose a name not already in this repository: preFlight imports a script as a module named
after its file, so two scripts with the same name cannot coexist. A name that collides
with a standard-library module (`json.py`, `os.py`) is refused by preFlight.

The script documents itself. No separate description file is required.

- The header lines in the table below.
- A docstring stating what the script changes and when to use it.
- Every value a user must tune as a named constant at the top of the file, with its unit,
  and a default that is safe to run untuned.
- Plain, readable Python. No obfuscated code, no binaries, no code fetched at run time.

A `README.md` in the script's folder is optional. Use it for photos or a tuning
walk-through.

| Header line | Meaning |
|---|---|
| `# preflight-api: 1` | The script API version the script was written against. preFlight reads this line and refuses a script that declares a newer API than the build provides. |
| `# modifies-gcode: yes` or `no` | Whether the script changes the exported file |
| `# firmware: any` or a list | The firmwares the script supports, when it emits commands only some understand |
| `# access: none` or a list | What the script touches outside preFlight: `files`, `network`, `process` |
| `# requires: numpy` | Packages to install first. Omit the line when there are none. |

Only the first line is read by preFlight. The others are for the people reading and
reviewing the script.

### Submitting

1. Fork the repository and add your folder.
2. Run the script in preFlight on a real model and verify the preview and the exported
   G-code. For a repeatable run that captures everything the script prints:

   ```
   preFlight-console.exe --allow-scripts --export-gcode -o out.gcode project.3mf > log.txt 2>&1
   ```

   On Linux and macOS, give the same options to the preFlight executable.
   `--allow-scripts` grants on the command line the consent the application asks for in
   its dialog.
3. Open a pull request describing what the script does and the printer, firmware and
   preFlight version you tested on.

By submitting, you confirm that you wrote the script or have the right to share it, and
that you release it under AGPLv3 or higher.

### Review

A maintainer reads the script and checks the header against the code, then runs it in
preFlight and inspects the G-code it produces. We may also ask for changes.

oozeBot may alter any script in this repository, before merging it or at any time after,
for safety or correctness, or to bring it in line with the template and the current API.
The license you grant by submitting allows this. Your name stays in the file header and in
the commit history, and our changes are commits of their own, so the history shows what
you wrote and what we changed.

Scripts we cannot validate, scripts that do more than their header declares, and scripts
that defeat a printer's safety features are declined. There is no fixed timeline.

After a merge, send fixes and improvements as new pull requests. A script that a later
preFlight release breaks, or that causes problems in practice, may be updated or removed.

## License

AGPLv3 or higher. See [LICENSE](LICENSE).
