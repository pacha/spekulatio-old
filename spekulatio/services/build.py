import logging as log

from spekulatio.models import Site
from spekulatio.models.filetrees import content_conf
from spekulatio.models.filetrees import template_conf


def build(build_path, content_path, template_paths, only_modified):
    """Generate site in build_path from the files in content_path and template_paths.

    Building the site involves two main steps:

        * Creating a site tree in memory in which each node represents a file or
          directory of the final site.
        * Traverse the site tree executing an action per node to actually
          create those files.
    """
    site = Site(build_path=build_path, only_modified=only_modified)

    # Gathering info from template directories
    for template_path in template_paths:
        log.info(f"Reading template directory: {template_path}")
        site.from_directory(template_path, template_conf)

    # Gathering info from content directory
    log.info(f"Reading content directory: {content_path}")
    site.from_directory(content_path, content_conf)

    log.info("Sorting nodes...")
    site.sort()

    log.info("Setting node relationships...")
    site.set_relationships()

    log.info("Writing files to build directory...")
    site.build()

    site.display_tree()

