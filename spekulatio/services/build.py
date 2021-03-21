import logging as log

from spekulatio.model import Site
from spekulatio.model import ActionMap


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
        site.from_directory(
            template_path,
            ActionMap(
                [
                    ("underscore_file", "ignore"),
                    ("scss", "compile_css"),
                    ("html", "ignore"),
                    ("any", "copy"),
                ]
            ),
        )

    # Gathering info from content directory
    log.info(f"Reading content directory: {content_path}")
    site.from_directory(
        content_path,
        ActionMap(
            [
                ("values_file", "process_values"),
                ("underscore_file", "ignore"),
                ("html", "render"),
                ("rst", "render"),
                ("md", "render"),
                ("json", "render"),
                ("yaml", "render"),
                ("scss", "compile_css"),
                ("any", "copy"),
            ]
        ),
    )

    log.info("Reading values and sorting nodes...")
    site.setup_nodes()

    log.info("Writing files to build directory...")
    site.build()

    site.display_tree()
