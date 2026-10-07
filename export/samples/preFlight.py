#/|/ Copyright (c) preFlight 2025+ oozeBot, LLC
#/|/
#/|/ Released under AGPLv3 or higher
#/|/
# preFlight scripting API type stub (preprocessing and Export to Script). GENERATED FILE, do not edit.
# Generated from preFlight 1.4.1, script API 1.
#
# Built by build_stubs.py from the pybind11 module in
# src/luminary/gcode/scripting/PreProcessor.cpp (bindings and their docstrings),
# the C++ enum headers (numeric values) and PrintConfig.hpp (Settings).
#
# Place this file next to your script so the editor resolves
# "import preFlight" for autocomplete. At slice time the embedded module
# takes precedence; this file is never executed by preFlight.
#
# Entry points a script may define:
#   def process(gcode: GCode) -> None       preprocessing, runs as a step of G-code generation
#   def export(gcode: ExportGCode) -> None  Export to Script, receives the final text

from __future__ import annotations

from enum import IntEnum
from typing import Callable, Dict, List, Optional, Tuple

version: str  # preFlight version string, e.g. "1.3.0"
api_version: int  # script API version this build implements; a script may declare "# preflight-api: N" and is refused when N is newer
exe_dir: str  # directory containing the running preFlight executable
user_packages_dir: str  # per-user pip target directory added to sys.path each slice, empty when unusable


class ScriptTimeout(BaseException):
    """Raised in a script that ran past the preprocessing time limit; the slice then fails. Do not catch it."""


class MoveType(IntEnum):
    """Kind of G-code move"""
    Noop = 0  # no operation
    Retract = 1  # filament retraction
    Unretract = 2  # filament unretraction
    Seam = 3  # seam point
    ToolChange = 4  # tool change (T command)
    ColorChange = 5  # color change event
    PausePrint = 6  # pause print event
    CustomGCode = 7  # custom G-code event
    Travel = 8  # non-extrusion travel
    Wipe = 9  # nozzle wipe
    Extrude = 10  # extrusion move


class ExtrusionRole(IntEnum):
    """Feature type of an extrusion move"""
    NoRole = 0  # no role assigned
    Serpentine = 1  # Serpentine single-path island fill
    SerpentineOverhang = 2  # Serpentine fill over an unsupported area
    Perimeter = 3  # inner perimeter
    ExternalPerimeter = 4  # outer perimeter (visible wall)
    OverhangPerimeter = 5  # perimeter over an unsupported area
    InterlockingPerimeter = 6  # interlocking boundary perimeter
    InternalInfill = 7  # sparse internal fill
    SolidInfill = 8  # solid fill that is not a top surface
    TopSolidInfill = 9  # top surface fill
    Ironing = 10  # ironing pass
    BridgeInfill = 11  # bridging fill over gaps
    GapFill = 12  # thin gap fill between features
    Skirt = 13  # skirt or brim outline
    SupportMaterial = 14  # support structure
    SupportMaterialInterface = 15  # support interface layer
    WipeTower = 16  # wipe tower purge
    Custom = 17  # custom G-code region, for example start or end G-code


class CustomEventType(IntEnum):
    """Kind of custom G-code event placed at a print Z"""
    ColorChange = 0  # M600 color change
    PausePrint = 1  # M601 pause
    ToolChange = 2  # tool change event
    Template = 3  # template custom G-code
    Custom = 4  # user custom G-code


class FilamentUsage:
    """Filament consumption for one extrusion role or extruder"""

    # Read-only
    meters: float  # filament length (m)
    grams: float  # filament weight (g)
    volume_mm3: float  # filament volume (mm3)
    cost: float  # filament cost in the configured currency


class CustomEvent:
    """A custom G-code event (color change, pause, ...) at a print Z"""

    # Read-only
    z: float  # print Z of the event (mm)
    type: int  # CustomEventType value
    extruder: int  # extruder index
    color: str  # color string
    extra: str  # custom G-code text


class Move:
    """A single G-code movement. Positions in mm, feedrates in mm/s, temperatures in C. Writable properties update both the move and its G-code line."""

    # Read/write
    feedrate: float  # commanded feedrate (mm/s), written back as the F parameter
    fan_speed: float  # fan percentage (0-100); a change emits M106 before the move and the original value is restored before the first unmodified extruding move that follows
    temperature: float  # hotend temperature (C); a change emits M104 before the move and the original value is restored before the first unmodified extruding move that follows, unless it reads 0 (unknown)
    delta_e: float  # filament displacement (mm), written back as the E parameter
    width: float  # extrusion line width (mm), preview only
    height: float  # extrusion height (mm), preview only
    annotation: str  # comment appended to this move's G-code line when it is modified, overrides gcode.annotation

    # Read-only
    type: MoveType  # kind of move
    role: ExtrusionRole  # feature type of the extrusion
    extruder_id: int  # active extruder (0-based)
    color_id: int  # sequential color change counter
    mm3_per_mm: float  # volumetric rate constant (mm3 per mm of path)
    actual_feedrate: float  # feedrate after acceleration limits (mm/s)
    gcode_line_id: int  # 1-based line of this move in the virtual G-code file
    layer_id: int  # index of the layer this move belongs to
    internal_only: bool  # True for internal G2/G3 arc segments
    x: float  # X position (mm)
    y: float  # Y position (mm)
    z: float  # Z position (mm)
    volumetric_rate: float  # feedrate * mm3_per_mm (mm3/s)
    actual_volumetric_rate: float  # actual_feedrate * mm3_per_mm (mm3/s)
    time: float  # move duration in seconds (normal mode)
    time_stealth: float  # move duration in seconds (stealth mode)
    distance: float  # XYZ path length (mm)
    junction_angle: float  # angle from the previous move (degrees, signed: positive right, negative left)
    acceleration: float  # effective acceleration (mm/s2, normal mode)
    acceleration_stealth: float  # effective acceleration (mm/s2, stealth mode)
    max_entry_speed: float  # junction-limited entry speed (mm/s, normal mode)
    max_entry_speed_stealth: float  # junction-limited entry speed (mm/s, stealth mode)
    region_area: float  # fill region area (mm2): island for perimeters, fill surface for infill, 0 if not applicable
    fill_pattern: str  # infill pattern name (Rectilinear, Gyroid, ...), empty for non-fill moves


class Layer:
    """All moves sharing one layer_id, with filters and layer-boundary G-code injection"""

    # Read-only
    id: int  # layer number
    z: float  # Z height of this layer (mm)
    height: float  # layer height (mm), delta from the previous layer
    time: float  # total layer time in seconds (normal mode)
    moves: List[Move]  # all moves in this layer
    first_line: int  # 1-based id of the first raw G-code line belonging to this layer (the line after the previous layer's last move, so the layer-change block is included)
    last_line: int  # 1-based id of the last raw G-code line of this layer (its last move); text after the final layer belongs to no layer

    def prepend(self, gcode: str, comment: str = '') -> None:
        """Insert G-code lines before the first move of this layer"""
        ...

    def append(self, gcode: str, comment: str = '') -> None:
        """Insert G-code lines after the last move of this layer"""
        ...

    def moves_by_type(self, move_type: MoveType) -> List[Move]:
        """Moves of this layer with the given type"""
        ...

    def moves_by_role(self, role: ExtrusionRole) -> List[Move]:
        """Moves of this layer with the given extrusion role"""
        ...

    def extrusion_length(self) -> float:
        """Total filament extruded in this layer (mm)"""
        ...

    def travel_distance(self) -> float:
        """Total travel (non-extrusion) distance in this layer (mm)"""
        ...

    def find_line(self, text: str) -> int:
        """1-based id of the first line of this layer containing text, 0 if none"""
        ...

    def find_lines(self, text: str) -> List[int]:
        """1-based ids of every line of this layer containing text"""
        ...

    def lines(self) -> List[Tuple[int, str]]:
        """every raw line of this layer as (line_id, text)"""
        ...


class Settings:
    """All slicer settings (print, filament and printer) merged into one namespace.

    Access as gcode.settings.key or gcode.settings["key"]; every value is the
    serialized string form of the option. Generated from PrintConfig.hpp.
    """

    auto_speed: str  # bool (0/1)
    autoemit_temperature_commands: str  # bool (0/1)
    automatic_extrusion_widths: str  # bool (0/1)
    automatic_infill_combination: str  # bool (0/1)
    automatic_infill_combination_max_layer_height: str  # float or percentage
    avoid_crossing_curled_overhangs: str  # bool (0/1)
    avoid_crossing_perimeters: str  # bool (0/1)
    avoid_crossing_perimeters_max_detour: str  # float or percentage
    bed_shape: str  # comma-separated XxY points
    bed_temperature: str  # comma-separated ints
    bed_temperature_extruder: str  # int
    before_layer_gcode: str
    between_objects_gcode: str
    binary_gcode: str  # bool (0/1)
    bottom_fill_pattern: str  # enum name
    bottom_solid_layers: str  # int
    bottom_solid_min_thickness: str  # float
    bridge_acceleration: str  # float
    bridge_angle: str  # float
    bridge_extrusion_width: str  # float or percentage
    bridge_fan_speed: str  # comma-separated ints
    bridge_flow_ratio: str  # float
    bridge_infill_overlap: str  # float or percentage
    bridge_infill_perimeter_overlap: str  # float or percentage
    bridge_speed: str  # float
    brim_ears_detection_length: str  # float
    brim_ears_max_angle: str  # float
    brim_separation: str  # float
    brim_type: str  # enum name
    brim_width: str  # float
    chamber_minimal_temperature: str  # comma-separated ints
    chamber_temperature: str  # comma-separated ints
    color_change_gcode: str
    color_mixing_base_extruder: str  # enum name
    color_mixing_base_layers: str  # int
    colorprint_heights: str  # comma-separated floats
    complete_objects: str  # bool (0/1)
    cooling: str  # comma-separated bools (0/1)
    cooling_perimeter_transition_distance: str  # comma-separated floats
    cooling_slowdown_logic: str  # comma-separated enum names
    cooling_tube_length: str  # float
    cooling_tube_retraction: str  # float
    currency_symbol: str
    custom_parameters_filament: str  # semicolon-separated strings
    custom_parameters_print: str
    custom_parameters_printer: str
    default_acceleration: str  # float
    deretract_speed: str  # comma-separated floats
    disable_fan_first_layers: str  # comma-separated ints
    dont_slow_down_outer_wall: str  # comma-separated bools (0/1)
    dont_support_bridges: str  # bool (0/1)
    draft_shield: str  # enum name
    duplicate_distance: str  # float
    elefant_foot_compensation: str  # float
    enable_dynamic_fan_speeds: str  # comma-separated bools (0/1)
    enable_dynamic_overhang_speeds: str  # bool (0/1)
    enable_manual_fan_speeds: str  # comma-separated bools (0/1)
    end_filament_gcode: str  # semicolon-separated strings
    end_gcode: str
    ensure_vertical_shell_thickness: str  # enum name
    export_script: str
    export_script_enabled: str  # bool (0/1)
    external_perimeter_acceleration: str  # float
    external_perimeter_extrusion_width: str  # float or percentage
    external_perimeter_overlap: str  # float or percentage
    external_perimeter_speed: str  # float or percentage
    external_perimeters_first: str  # bool (0/1)
    extra_loading_move: str  # float
    extra_perimeters: str  # bool (0/1)
    extra_perimeters_on_overhangs: str  # bool (0/1)
    extruder_clearance_height: str  # float
    extruder_clearance_radius: str  # float
    extruder_colour: str  # semicolon-separated strings
    extruder_offset: str  # comma-separated XxY points
    extrusion_axis: str
    extrusion_multiplier: str  # comma-separated floats
    extrusion_width: str  # float or percentage
    extrusion_width_percent_of_nozzle: str  # bool (0/1)
    fan_always_on: str  # comma-separated bools (0/1)
    fan_below_layer_time: str  # comma-separated ints
    fan_spinup_bridge_infill: str  # comma-separated bools (0/1)
    fan_spinup_overhang_perimeter: str  # comma-separated bools (0/1)
    fan_spinup_response_type: str  # comma-separated enum names
    fan_spinup_serpentine_overhang: str  # comma-separated bools (0/1)
    fan_spinup_time: str  # comma-separated ints
    filament_abrasive: str  # comma-separated bools (0/1)
    filament_colour: str  # semicolon-separated strings
    filament_cooling_final_speed: str  # comma-separated floats
    filament_cooling_initial_speed: str  # comma-separated floats
    filament_cooling_moves: str  # comma-separated ints
    filament_cost: str  # comma-separated floats
    filament_density: str  # comma-separated floats
    filament_diameter: str  # comma-separated floats
    filament_enable_pressure_advance: str  # comma-separated bools (0/1)
    filament_infill_max_crossing_speed: str  # comma-separated floats
    filament_infill_max_speed: str  # comma-separated floats
    filament_load_time: str  # comma-separated floats
    filament_loading_speed: str  # comma-separated floats
    filament_loading_speed_start: str  # comma-separated floats
    filament_max_print_speed: str  # comma-separated floats
    filament_max_volumetric_flow: str  # comma-separated floats
    filament_max_volumetric_speed: str  # comma-separated floats
    filament_minimal_purge_on_wipe_tower: str  # comma-separated floats
    filament_multitool_ramming: str  # comma-separated bools (0/1)
    filament_multitool_ramming_flow: str  # comma-separated floats
    filament_multitool_ramming_volume: str  # comma-separated floats
    filament_notes: str  # semicolon-separated strings
    filament_pressure_advance: str  # comma-separated floats
    filament_purge_multiplier: str  # comma-separated percentages
    filament_ramming_parameters: str  # semicolon-separated strings
    filament_seam_gap_distance: str  # comma-separated floats or percentages, nil when unset
    filament_shrinkage_compensation_x: str  # comma-separated percentages
    filament_shrinkage_compensation_y: str  # comma-separated percentages
    filament_shrinkage_compensation_z: str  # comma-separated percentages
    filament_soluble: str  # comma-separated bools (0/1)
    filament_spool_weight: str  # comma-separated floats
    filament_stamping_distance: str  # comma-separated floats
    filament_stamping_loading_speed: str  # comma-separated floats
    filament_toolchange_delay: str  # comma-separated floats
    filament_transmission_distance: str  # comma-separated floats
    filament_type: str  # semicolon-separated strings
    filament_unload_time: str  # comma-separated floats
    filament_unloading_speed: str  # comma-separated floats
    filament_unloading_speed_start: str  # comma-separated floats
    fill_angle: str  # float
    fill_density: str  # percentage
    fill_pattern: str  # enum name
    first_layer_acceleration: str  # float
    first_layer_acceleration_over_raft: str  # float
    first_layer_bed_temperature: str  # comma-separated ints
    first_layer_extrusion_width: str  # float or percentage
    first_layer_height: str  # float or percentage
    first_layer_infill_speed: str  # float or percentage
    first_layer_speed: str  # float or percentage
    first_layer_speed_over_raft: str  # float or percentage
    first_layer_temperature: str  # comma-separated ints
    first_layer_travel_speed: str  # float or percentage
    first_travel_combine_z: str  # bool (0/1)
    full_fan_speed_layer: str  # comma-separated ints
    fuzzy_skin: str  # enum name
    fuzzy_skin_first_layer: str  # bool (0/1)
    fuzzy_skin_mode: str  # enum name
    fuzzy_skin_noise_type: str  # enum name
    fuzzy_skin_octaves: str  # int
    fuzzy_skin_on_top: str  # bool (0/1)
    fuzzy_skin_painted_perimeters: str  # enum name
    fuzzy_skin_persistence: str  # float
    fuzzy_skin_point_dist: str  # float
    fuzzy_skin_point_placement: str  # enum name
    fuzzy_skin_scale: str  # float
    fuzzy_skin_thickness: str  # float
    fuzzy_skin_visibility_detection: str  # enum name
    gcode_comments: str  # bool (0/1)
    gcode_flavor: str  # enum name
    gcode_label_objects: str  # enum name
    gcode_resolution: str  # float
    gcode_substitutions: str  # semicolon-separated strings
    high_current_on_filament_swap: str  # bool (0/1)
    idle_temperature: str  # comma-separated ints, nil when unset
    infill_acceleration: str  # float
    infill_anchor: str  # float or percentage
    infill_anchor_max: str  # float or percentage
    infill_every_layers: str  # int
    infill_extruder: str  # int
    infill_extrusion_width: str  # float or percentage
    infill_first: str  # bool (0/1)
    infill_overlap: str  # float or percentage
    infill_speed: str  # float
    interface_shells: str  # bool (0/1)
    interlock_flow_detection: str  # enum name
    interlock_perimeter_count: str  # int
    interlock_perimeter_overlap: str  # float or percentage
    interlock_perimeters_enabled: str  # bool (0/1)
    interlock_regular_perimeters: str  # int
    interlock_solid_layers_bottom: str  # int
    interlock_solid_layers_top: str  # int
    interlocking_beam: str  # bool (0/1)
    interlocking_beam_layer_count: str  # int
    interlocking_beam_width: str  # float
    interlocking_boundary_avoidance: str  # int
    interlocking_depth: str  # int
    interlocking_orientation: str  # float
    interlocking_perimeter_extruder: str  # int
    ironing: str  # bool (0/1)
    ironing_flowrate: str  # percentage
    ironing_spacing: str  # float
    ironing_speed: str  # float
    ironing_type: str  # enum name
    layer_gcode: str
    layer_height: str  # float
    machine_klipper_max_accel: str  # float
    machine_klipper_max_velocity: str  # float
    machine_klipper_minimum_cruise_ratio: str  # float
    machine_klipper_square_corner_velocity: str  # float
    machine_limits_usage: str  # enum name
    machine_max_acceleration_e: str  # comma-separated floats
    machine_max_acceleration_extruding: str  # comma-separated floats
    machine_max_acceleration_retracting: str  # comma-separated floats
    machine_max_acceleration_travel: str  # comma-separated floats
    machine_max_acceleration_x: str  # comma-separated floats
    machine_max_acceleration_y: str  # comma-separated floats
    machine_max_acceleration_z: str  # comma-separated floats
    machine_max_feedrate_e: str  # comma-separated floats
    machine_max_feedrate_x: str  # comma-separated floats
    machine_max_feedrate_y: str  # comma-separated floats
    machine_max_feedrate_z: str  # comma-separated floats
    machine_max_jerk_e: str  # comma-separated floats
    machine_max_jerk_x: str  # comma-separated floats
    machine_max_jerk_y: str  # comma-separated floats
    machine_max_jerk_z: str  # comma-separated floats
    machine_max_junction_deviation: str  # comma-separated floats
    machine_min_extruding_rate: str  # comma-separated floats
    machine_min_travel_rate: str  # comma-separated floats
    machine_rrf_m201: str
    machine_rrf_m203: str
    machine_rrf_m204: str
    machine_rrf_m207: str
    machine_rrf_m566: str
    machine_time_compensation: str  # percentage
    manual_fan_speed_external_perimeter: str  # comma-separated ints
    manual_fan_speed_interlocking_perimeter: str  # comma-separated ints
    manual_fan_speed_internal_infill: str  # comma-separated ints
    manual_fan_speed_ironing: str  # comma-separated ints
    manual_fan_speed_overhang_perimeter: str  # comma-separated ints
    manual_fan_speed_perimeter: str  # comma-separated ints
    manual_fan_speed_serpentine: str  # comma-separated ints
    manual_fan_speed_serpentine_overhang: str  # comma-separated ints
    manual_fan_speed_skirt: str  # comma-separated ints
    manual_fan_speed_solid_infill: str  # comma-separated ints
    manual_fan_speed_support_interface: str  # comma-separated ints
    manual_fan_speed_support_material: str  # comma-separated ints
    manual_fan_speed_top_solid_infill: str  # comma-separated ints
    max_fan_speed: str  # comma-separated ints
    max_layer_height: str  # comma-separated floats
    max_perimeter_width: str  # percentage
    max_print_height: str  # float
    max_print_speed: str  # float
    max_volumetric_extrusion_rate_slope_negative: str  # float
    max_volumetric_extrusion_rate_slope_positive: str  # float
    max_volumetric_flow: str  # float
    max_volumetric_speed: str  # float
    merge_top_solid_infills: str  # bool (0/1)
    min_bead_width: str  # float or percentage
    min_fan_speed: str  # comma-separated ints
    min_feature_size: str  # float or percentage
    min_layer_height: str  # comma-separated floats
    min_print_speed: str  # comma-separated floats
    min_skirt_length: str  # float
    min_wall_length: str  # float or percentage
    mmu_segmented_region_interlocking_depth: str  # float
    mmu_segmented_region_max_width: str  # float
    multimaterial_purging: str  # float
    narrow_to_athena: str  # bool (0/1)
    narrow_to_athena_threshold: str  # float
    narrow_to_athena_top_bottom: str  # bool (0/1)
    notes: str
    nozzle_diameter: str  # comma-separated floats
    nozzle_high_flow: str  # comma-separated bools (0/1)
    nozzle_width_warning_max: str  # comma-separated percentages
    nozzle_width_warning_min: str  # comma-separated percentages
    only_one_perimeter_first_layer: str  # bool (0/1)
    only_retract_when_crossing_perimeters: str  # bool (0/1)
    ooze_prevention: str  # bool (0/1)
    output_filename_format: str
    over_bridge_speed: str  # float or percentage
    overhang_fan_speed_0: str  # comma-separated ints
    overhang_fan_speed_1: str  # comma-separated ints
    overhang_fan_speed_2: str  # comma-separated ints
    overhang_fan_speed_3: str  # comma-separated ints
    overhang_speed_0: str  # float or percentage
    overhang_speed_1: str  # float or percentage
    overhang_speed_2: str  # float or percentage
    overhang_speed_3: str  # float or percentage
    overhangs: str  # bool (0/1)
    parking_pos_retraction: str  # float
    pause_print_gcode: str
    perimeter_acceleration: str  # float
    perimeter_compression: str  # enum name
    perimeter_extruder: str  # int
    perimeter_extrusion_width: str  # float or percentage
    perimeter_generator: str  # enum name
    perimeter_perimeter_overlap: str  # float or percentage
    perimeter_speed: str  # float
    perimeters: str  # int
    post_process: str  # semicolon-separated strings
    prefer_clockwise_movements: str  # bool (0/1)
    preprocessing_enabled_filament: str  # bool (0/1)
    preprocessing_enabled_print: str  # bool (0/1)
    preprocessing_enabled_printer: str  # bool (0/1)
    preprocessing_scripts_filament: str  # semicolon-separated strings
    preprocessing_scripts_print: str  # semicolon-separated strings
    preprocessing_scripts_printer: str  # semicolon-separated strings
    print_high_flow_nozzle: str  # comma-separated bools (0/1)
    print_nozzle_diameters: str  # comma-separated floats
    printer_model: str
    printer_notes: str
    raft_contact_distance: str  # float
    raft_expansion: str  # float
    raft_first_layer_density: str  # percentage
    raft_first_layer_expansion: str  # float
    raft_layers: str  # int
    remaining_times: str  # bool (0/1)
    resolution: str  # float
    retract_before_travel: str  # comma-separated floats
    retract_before_wipe: str  # comma-separated percentages
    retract_layer_change: str  # comma-separated bools (0/1)
    retract_length: str  # comma-separated floats
    retract_length_toolchange: str  # comma-separated floats
    retract_lift: str  # comma-separated floats
    retract_lift_above: str  # comma-separated floats
    retract_lift_below: str  # comma-separated floats
    retract_restart_extra: str  # comma-separated floats
    retract_restart_extra_toolchange: str  # comma-separated floats
    retract_speed: str  # comma-separated floats
    scarf_seam_entire_loop: str  # bool (0/1)
    scarf_seam_length: str  # float
    scarf_seam_max_segment_length: str  # float
    scarf_seam_on_inner_perimeters: str  # bool (0/1)
    scarf_seam_only_on_smooth: str  # bool (0/1)
    scarf_seam_placement: str  # enum name
    scarf_seam_start_height: str  # percentage
    seam_gap_distance: str  # float or percentage
    seam_notch_angle: str  # float
    seam_notch_width: str  # float
    seam_position: str  # enum name
    seam_type: str  # enum name
    serpentine_aim: str  # enum name
    serpentine_depth: str  # float
    serpentine_enabled: str  # bool (0/1)
    serpentine_extrusion_width: str  # float or percentage
    serpentine_limit_depth: str  # bool (0/1)
    serpentine_max_bead: str  # percentage
    serpentine_outer_loop: str  # bool (0/1)
    serpentine_overlap: str  # float or percentage
    serpentine_relaxed: str  # bool (0/1)
    serpentine_ridges: str  # enum name
    serpentine_solid_surfaces: str  # bool (0/1)
    serpentine_spacing: str  # float
    silent_mode: str  # bool (0/1)
    single_extruder_multi_material: str  # bool (0/1)
    single_extruder_multi_material_priming: str  # bool (0/1)
    skirt_distance: str  # float
    skirt_height: str  # int
    skirts: str  # int
    slice_closing_radius: str  # float
    slicing_mode: str  # enum name
    slowdown_below_layer_time: str  # comma-separated ints
    small_perimeter_diameter: str  # float
    small_perimeter_speed: str  # float or percentage
    solid_fill_pattern: str  # enum name
    solid_infill_acceleration: str  # float
    solid_infill_below_area: str  # float
    solid_infill_every_layers: str  # int
    solid_infill_extruder: str  # int
    solid_infill_extrusion_width: str  # float or percentage
    solid_infill_speed: str  # float or percentage
    spiral_vase: str  # bool (0/1)
    staggered_inner_seams: str  # bool (0/1)
    standby_temperature_delta: str  # int
    start_filament_gcode: str  # semicolon-separated strings
    start_gcode: str
    support_alerts: str  # bool (0/1)
    support_baobab_angle: str  # float
    support_baobab_angle_slow: str  # float
    support_baobab_canopy_density: str  # percentage
    support_baobab_max_canopy_angle: str  # float
    support_baobab_min_opening: str  # float
    support_baobab_plant_on_model: str  # bool (0/1)
    support_baobab_trunk_consolidation: str  # float
    support_baobab_trunk_diameter: str  # float
    support_baobab_trunk_diameter_angle: str  # float
    support_baobab_trunk_distance: str  # float
    support_material: str  # bool (0/1)
    support_material_angle: str  # float
    support_material_auto: str  # bool (0/1)
    support_material_bottom_contact_distance: str  # enum name
    support_material_bottom_contact_extrusion_width: str  # percentage
    support_material_bottom_interface_layers: str  # int
    support_material_bridge_no_gap: str  # bool (0/1)
    support_material_buildplate_only: str  # bool (0/1)
    support_material_closing_radius: str  # float
    support_material_contact_distance: str  # enum name
    support_material_contact_distance_custom: str  # float
    support_material_enforce_layers: str  # int
    support_material_extruder: str  # int
    support_material_extrusion_width: str  # float or percentage
    support_material_interface_contact_loops: str  # bool (0/1)
    support_material_interface_extruder: str  # int
    support_material_interface_extrusion_width: str  # float or percentage
    support_material_interface_layers: str  # int
    support_material_interface_pattern: str  # enum name
    support_material_interface_spacing: str  # float
    support_material_interface_speed: str  # float or percentage
    support_material_min_area: str  # float
    support_material_pattern: str  # enum name
    support_material_spacing: str  # float
    support_material_speed: str  # float
    support_material_style: str  # enum name
    support_material_threshold: str  # int
    support_material_top_contact_extrusion_width: str  # percentage
    support_material_with_sheath: str  # bool (0/1)
    support_material_xy_spacing: str  # float or percentage
    support_tree_angle: str  # float
    support_tree_angle_slow: str  # float
    support_tree_branch_diameter: str  # float
    support_tree_branch_diameter_angle: str  # float
    support_tree_branch_diameter_double_wall: str  # float
    support_tree_branch_distance: str  # float
    support_tree_min_opening: str  # float
    support_tree_tip_diameter: str  # float
    support_tree_top_rate: str  # percentage
    temperature: str  # comma-separated ints
    template_custom_gcode: str
    thin_wall_precision: str  # enum name
    thumbnails: str
    thumbnails_format: str  # enum name
    time_cost: str  # float
    toolchange_gcode: str
    top_fill_pattern: str  # enum name
    top_infill_extrusion_width: str  # float or percentage
    top_one_perimeter_type: str  # enum name
    top_solid_infill_acceleration: str  # float
    top_solid_infill_speed: str  # float or percentage
    top_solid_layers: str  # int
    top_solid_min_thickness: str  # float
    top_surface_flow_reduction: str  # percentage
    top_surface_visibility_detection: str  # enum name
    travel_acceleration: str  # float
    travel_lift_before_obstacle: str  # comma-separated bools (0/1)
    travel_max_lift: str  # comma-separated floats
    travel_ramping_lift: str  # comma-separated bools (0/1)
    travel_short_distance_acceleration: str  # float
    travel_slope: str  # comma-separated floats
    travel_speed: str  # float
    travel_speed_z: str  # float
    use_firmware_retraction: str  # bool (0/1)
    use_relative_e_distances: str  # bool (0/1)
    use_volumetric_e: str  # bool (0/1)
    variable_layer_height: str  # bool (0/1)
    wall_distribution_count: str  # int
    wall_transition_angle: str  # float
    wall_transition_filter_deviation: str  # float or percentage
    wall_transition_length: str  # float or percentage
    wipe: str  # comma-separated bools (0/1)
    wipe_extend: str  # comma-separated bools (0/1)
    wipe_into_infill: str  # bool (0/1)
    wipe_into_objects: str  # bool (0/1)
    wipe_length: str  # comma-separated floats
    wipe_tower: str  # bool (0/1)
    wipe_tower_acceleration: str  # float
    wipe_tower_bridging: str  # float
    wipe_tower_brim_width: str  # float
    wipe_tower_cone_angle: str  # float
    wipe_tower_extra_flow: str  # percentage
    wipe_tower_extra_spacing: str  # percentage
    wipe_tower_extruder: str  # int
    wipe_tower_no_sparse_layers: str  # bool (0/1)
    wipe_tower_width: str  # float
    wiping_volumes_matrix: str  # comma-separated floats
    wiping_volumes_use_custom_matrix: str  # bool (0/1)
    xy_size_compensation: str  # float
    z_offset: str  # float


class GCode:
    """The G-code being generated, handed to process(): layers, moves, statistics, settings and raw line editing"""

    # Read/write
    annotation: str  # comment appended to every modified G-code line whose move has no annotation of its own

    # Read-only
    layers: List[Layer]  # all layers, indexed by layer_id
    max_print_height: float  # maximum print height (mm)
    extruder_count: int  # number of extruders
    extruder_colors: List[str]  # extruder colors as hex strings (#FF8000)
    spiral_vase_mode: bool  # True if spiral vase mode is active
    time_estimate_normal: float  # total estimated print time in seconds (normal mode)
    time_estimate_stealth: float  # total estimated print time in seconds (stealth mode)
    first_layer_time: float  # first layer time in seconds
    filament_cost: List[float]  # filament cost per extruder
    time_cost: float  # machine time cost rate
    currency_symbol: str  # currency symbol, e.g. $
    preset_print: str  # active print profile name
    preset_filament: List[str]  # active filament profile names
    preset_printer: str  # active printer profile name
    moves: List[Move]  # flat list of all live moves (removed and dead entries excluded)
    line_count: int  # number of lines in the virtual G-code file
    z_offset: float  # Z offset (mm)
    bed_shape: List[Tuple[float, float]]  # bed outline as (x, y) points
    settings: Settings  # every print, filament and printer setting as a string, by attribute or key
    filament_diameters: List[float]  # filament diameter per extruder (mm)
    filament_densities: List[float]  # filament density per extruder (g/cm3)
    filament_by_role: Dict[ExtrusionRole, FilamentUsage]  # filament usage per extrusion role
    filament_by_extruder: Dict[int, FilamentUsage]  # filament usage per extruder
    filament_by_color_change: List[float]  # filament volume (mm3) per color change segment
    custom_events: List[CustomEvent]  # custom G-code events (color changes, pauses, ...) by print Z
    role_metrics: Dict[ExtrusionRole, dict]  # per-role {max_commands_per_sec, max_layer}
    overall_metrics: dict  # {max_commands_per_sec, max_layer} over the whole print
    conflict: Optional[dict]  # {object1, object2, height, layer} of the first object collision, or None

    def insert(self, line: int, gcode: str, position: str = 'after', comment: str = '') -> None:
        """Insert raw G-code after (default) or before the given 1-based line; comment is appended as '; comment'"""
        ...

    def get_line(self, line_id: int) -> str:
        """Text of a raw G-code line (1-based), empty if out of range"""
        ...

    def rewrite(self, line_id: int, gcode: str, comment: str = '') -> None:
        """Replace a raw G-code line (1-based)"""
        ...

    def find_line(self, text: str, start: int = 1, end: int = 0) -> int:
        """1-based id of the first line containing text within lines start..end (end 0 = last line), 0 if none"""
        ...

    def find_lines(self, text: str, start: int = 1, end: int = 0) -> List[int]:
        """1-based ids of every line containing text within lines start..end (end 0 = last line)"""
        ...

    def find_moves(self, type: Optional[MoveType] = None, role: Optional[ExtrusionRole] = None, extruder: Optional[int] = None, z_min: Optional[float] = None, z_max: Optional[float] = None) -> List[Move]:
        """Moves matching every given filter"""
        ...

    def remove_moves(self, predicate: Callable[[Move], bool]) -> int:
        """Remove every move for which predicate returns True and return the count"""
        ...


class ExportGCode:
    """The final G-code handed to an Export to Script export() function"""

    # Read/write
    data: List[str]  # G-code lines, each with its trailing newline

    # Read-only
    filename: str  # suggested output filename, from the output filename format
