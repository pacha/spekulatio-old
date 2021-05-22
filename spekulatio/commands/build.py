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
    "content_dirs",
    multiple=True,
    default=[],
    help="Add directory for content files (default: ./content).",
)
@click.option(
    "-t",
    "--template-dir",
    "template_dirs",
    multiple=True,
    default=[],
    help="Add directory for HTML templates (default: ./templates).",
)
@click.option(
    "-d",
    "--data-dir",
    "data_dirs",
    multiple=True,
    default=[],
    help="Add directory for data files (default: ./data).",
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
def build(build_dir, content_dirs, template_dirs, data_dirs, only_modified, verbose, very_verbose):
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
    except PermissionError:
        log.error(f"Can't create build directory '{build_dir}': permission error")
        sys.exit(1)

    # define relevant paths
    current_path = Path('.')
    spekulatio_path = Path(__file__).absolute().parent.parent.parent
    spekulatio_templates_path = spekulatio_path / 'data' / "template-dirs"

    # check input directories
    content_paths = []
    template_paths = []
    data_paths = []
    if any([content_dirs, template_dirs, data_dirs]):

        # content dirs
        for content_dir in content_dirs:
            content_path = Path(content_dir)
            if not content_path.is_dir():
                log.error(f"Content directory '{content_dir}' not found.")
                sys.exit(1)
            content_paths.append(content_path)
            log.info(f"Added content directory: {content_path}")

        # template dirs
        for template_dir in template_dirs:
            for root_path in [current_path, spekulatio_templates_path]:
                template_path = root_path / template_dir
                if template_path.is_dir():
                    template_paths.append(template_path)
                    log.info(f"Added template directory: {template_path}")
                    break
            else:
                log.error(f"Template directory '{template_dir}' not found.")
                sys.exit(1)

        # data dirs
        for data_dir in data_dirs:
            data_path = Path(data_dir)
            if not data_path.is_dir():
                log.error(f"Data directory '{data_dir}' not found.")
                sys.exit(1)
            data_paths.append(data_path)
            log.info(f"Added data directory: {data_path}")

    else:

        # default content
        default_content_path = Path("./content")
        if default_content_path.is_dir():
            content_paths.append(default_content_path)
            log.info(f"Added content directory: {default_content_path}")

        # default templates
        default_template_path = Path("./templates")
        if default_template_path.is_dir():
            template_paths.append(default_template_path)
            log.info(f"Added template directory: {default_template_path}")

        # default data
        default_data_path = Path("./data")
        if default_data_path.is_dir():
            data_paths.append(default_data_path)
            log.info(f"Added data directory: {default_data_path}")

        if not any([content_paths, template_paths, data_paths]):
            log.error(
                "No input directories provided and none of the default ones "
                "('content', 'templates' or 'data') found in current directory."
            )
            sys.exit(1)

    # add default Spekulatio's default templates
    spekulatio_default_template_path = spekulatio_templates_path / "spekulatio-default"
    template_paths.insert(0, spekulatio_default_template_path)
    log.info(f"Added template directory: {spekulatio_default_template_path} with the lowest priority.")

    # finally: build site
    try:
        services.build(build_path, content_paths, template_paths, data_paths, only_modified)
    except SpekulatioError as err:
        log.error(f"{err}")
        sys.exit(1)

    log.info(f"Done.")
