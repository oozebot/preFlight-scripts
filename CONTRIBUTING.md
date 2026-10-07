# Contributing a script

Scripts are contributed by pull request to this repository. The full guide is the
[Contributing a script](README.md#contributing-a-script) section of the README. In short:

- One `.py` file in `preprocessor/community/<script_name>/` or
  `export/community/<script_name>/`, started from `process_template.py` or
  `export_template.py`.
- The header lines filled in, a docstring, and every tunable as a named constant at the top
  of the file with a default that is safe to run untuned.
- Tested in preFlight on a real model, with the preview and the exported G-code checked.
- Released under AGPLv3 or higher.

Questions about scripting go to the main repository's
[Discussions](https://github.com/oozebot/preFlight/discussions), and problems to its
[Issues](https://github.com/oozebot/preFlight/issues).
