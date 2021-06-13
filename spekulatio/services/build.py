import logging as log

from spekulatio.models import Site
from spekulatio.models.filetrees import data_conf
from spekulatio.models.filetrees import template_conf
from spekulatio.models.filetrees import content_conf


def build(build_path, content_paths, template_paths, data_paths, only_modified):
    """Generate site in build_path by merging and processing the files in the filetrees provided.

    Building the site involves two main steps:

        * Creating a site tree in memory in which each node represents a file or
          directory of the final site.
        * Traverse the site tree executing an action per node to actually
          create those files.
    """
    site = Site(build_path=build_path, only_modified=only_modified)

    # Gathering info from data directories
    for data_path in data_paths:
        log.info(f"Reading data directory: {data_path}")
        site.from_directory(data_path, data_conf)

    # Gathering info from template directories
    for template_path in template_paths:
        log.info(f"Reading template directory: {template_path}")
        site.from_directory(template_path, template_conf)

    # Gathering info from content directories
    for content_path in content_paths:
        log.info(f"Reading content directory: {content_path}")
        site.from_directory(content_path, content_conf)

    log.info("Set values in nodes...")
    site.set_values()

    log.info("Sorting nodes...")
    site.sort()

    log.info("Setting node relationships...")
    site.set_relationships()

    log.info("Extracting content from nodes...")
    site.render_content()

    log.info("Writing files to build directory...")
    site.build()

    site.display_tree()
