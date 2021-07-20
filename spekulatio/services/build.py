import logging as log

from spekulatio.models import Site


def build(output_path, input_dirs, only_modified):
    """Generate site in output_path by merging and processing the files in the provided input directories.

    Building the site involves two main steps:

        * Creating a site tree in memory in which each node represents a file or
          directory of the final site.
        * Traverse the site tree executing an action per node to actually
          create those files.
    """
    site = Site(output_path=output_path, only_modified=only_modified)

    # merge directories into a single in-memory site tree
    for input_dir in input_dirs:
        log.info(f"Reading directory: {input_dir}")
        site.from_directory(input_dir)

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
