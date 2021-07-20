import sys
import logging as log
from pathlib import Path

import click
import coloredlogs

from spekulatio import services
from spekulatio.paths import spekulatio_templates_path
from spekulatio.paths import default_input_dir_path
from spekulatio.exceptions import SpekulatioError
from spekulatio.exceptions import SpekulatioConfigError
from spekulatio.models import InputDir
from spekulatio.models import get_input_dir_path
from spekulatio.models import FiletypeMap
from spekulatio.models import filetype_presets
from .config import get_config
from .config import get_project_and_config_paths


@click.command()
@click.option(
    "-c",
    "--config",
    "custom_config_location",
    help="Configuration file to use (default: ./spekulatio.yaml)",
)
@click.option(
    "--only-modified",
    default=False,
    is_flag=True,
    help="Regenerate only static and content files that have been modified.",
)
@click.option(
    "-v", "--verbose", default=False, is_flag=True, help="Show processing messages."
)
@click.option(
    "-vv", "--very-verbose", default=False, is_flag=True, help="Show debug information."
)
def build(
    custom_config_location,
    only_modified,
    verbose,
    very_verbose,
):
    """Build site."""

    # configure logging
    if very_verbose:
        log_level = log.DEBUG
    elif verbose:
        log_level = log.INFO
    else:
        log_level = log.WARN
    coloredlogs.install(fmt="%(levelname)8s | %(message)s", level=log_level)

    # log cache behavior
    if only_modified:
        log.info(f"Building only modified files (only_modified)")
    else:
        log.info(f"Building entire site (only_modified=false)")

    # get project and config_paths
    try:
        project_path, config_path = get_project_and_config_paths(custom_config_location)
        if config_path:
            log.info(f"Using configuration file: {config_path}")
        else:
            log.info(f"No configuration file provided. Using default configuration.")
    except FileNotFoundError:
        log.error(f"Configuration file '{custom_config_location}' not found.")
        sys.exit(1)

    # get spekulatio path (relative input dirs will be searched here)
    spekulatio_path = [
        project_path,
        spekulatio_templates_path,
    ]
    log.debug(f"Spekulatio path:")
    for path in spekulatio_path:
        log.debug(f"- {path}")

    # get configuration
    try:
        config = get_config(project_path, config_path)
    except SpekulatioConfigError as err:
        log.error("Error while reading configuration file:")
        for line in str(err).splitlines():
            if line.strip():
                log.error(" " + line)
        sys.exit(1)

    # get filetypes
    filetype_map = FiletypeMap()
    filetype_map.update(filetype_presets)
    if "filetypes" in config:
        filetype_map.update(config["filetypes"])
    log.debug(f"Defined filetypes:")
    log.debug(f"- <underscore_file>: ^_.+")
    log.debug(f"- <virtual_node>: ^.+\\.meta\\.(yaml|yaml)$")
    for filetype in filetype_map.map.values():
        log.debug(f"- {filetype.name}: {filetype.pattern.pattern}")

    # get output directory
    output_dir = config["output_dir"]
    log.info(f"Output directory: {output_dir}")
    output_path = Path(output_dir)
    try:
        output_path.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        log.error(f"Can't create output directory '{output_dir}': permission error")
        sys.exit(1)

    # add default input directory
    input_dirs = []
    default_input_dir = InputDir(
        path=default_input_dir_path,
        preset_name="site_templates",
        filetype_map=filetype_map,
    )
    input_dirs.append(default_input_dir)

    # add user input directorires
    for input_dir_dict in config["input_dirs"]:
        try:
            path_name = input_dir_dict["path"]
            preset_name = input_dir_dict.get("preset")
            action_dicts = input_dir_dict.get("actions")
            default_action_name = input_dir_dict.get("default_action")

            input_dir = InputDir(
                path=get_input_dir_path(path_name, spekulatio_path),
                preset_name=preset_name,
                filetype_map=filetype_map,
                action_dicts=action_dicts,
                default_action_name=default_action_name,
            )
        except SpekulatioConfigError as err:
            log.error(f"Error while processing input directories: {err}")
            sys.exit(1)
        else:
            input_dirs.append(input_dir)

    log.info(f"Input directories:")
    for input_dir in input_dirs:
        log.info(f"- {input_dir}")
        for filetype_name, action in input_dir.action_map.map.items():
            log.debug(f"  - {filetype_name}: {action.__name__.split('.')[-1]}")
        log.debug(
            f"  - <default action>: {input_dir.action_map.default_action.__name__.split('.')[-1]}"
        )

    # finally: build site
    try:
        services.build(output_path, input_dirs, only_modified)
    except SpekulatioError as err:
        log.error(f"{err}")
        sys.exit(1)

    log.info(f"Done.")
