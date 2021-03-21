import sys
import logging as log
from pathlib import Path

import click
import coloredlogs

from spekulatio import services
from spekulatio.exceptions import SpekulatioError


@click.command()
@click.option(
    "-b",
    "--build-dir",
    default="./build",
    help="Directory for output files (default: ./build).",
)
@click.option(
    "-c",
    "--content-dir",
    default="./content",
    help="Directory for content files (default: ./content).",
)
@click.option(
    "-t",
    "--template-dir",
    "template_dirs",
    default=["./templates"],
    multiple=True,
    help="Directory for HTML templates (default: ./templates).",
)
@click.option(
    "--only-modified",
    default=False,
    is_flag=True,
    help="Regenerate only static and content files that have been modified.",
)
@click.option(
    "--verbose", default=False, is_flag=True, help="Show processing messages."
)
@click.option(
    "--very-verbose", default=False, is_flag=True, help="Show debug information."
)
def build(build_dir, content_dir, template_dirs, only_modified, verbose, very_verbose):
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

    # check build directory
    log.info(f"Build directory: {build_dir}")
    build_path = Path(build_dir)
    try:
        build_path.mkdir(parents=True, exist_ok=True)
    except FileExistsError:
        log.error(f"Can't create build directory '{build_dir}': name already in use")
        sys.exit(1)
    except PermissionError:
        log.error(f"Can't create build directory '{build_dir}': permission error")
        sys.exit(1)

    # check content directory
    log.info(f"Content directory: {content_dir}")
    content_path = Path(content_dir)
    if not content_path.is_dir():
        log.error(f"Content directory '{content_path}' not found.")
        sys.exit(1)

    # check template directories
    template_paths = []
    for template_dir in template_dirs:
        template_path = Path(template_dir)
        if not template_path.is_dir():
            # if the default template directory is not present, it is just a warning
            if template_dir == "./templates":
                continue
            else:
                log.error(f"Template directory '{template_path}' not found.")
                sys.exit(1)
        template_paths.append(template_path)

    # add default template directory
    current_path = Path(__file__).absolute().parent.parent.parent
    default_template_path = current_path / 'data' / "default_templates"
    template_paths.append(default_template_path)

    # log all template directories
    for template_path in template_paths:
        log.info(f"Added template directory: {template_path}")

    # finally: build site
    try:
        services.build(build_path, content_path, template_paths, only_modified)
    except SpekulatioError as err:
        log.error(f"{err}")
        sys.exit(1)

    log.info(f"Done.")
