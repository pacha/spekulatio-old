import logging as log
from pathlib import Path

import sass

extension_change = ".css"


def extract_values(node, site):
    return {}

def extract_content(node, site):
    return {}


def build(src_path, dst_path, node, site):
    """Compile SCSS into CSS."""

    # get environment for the sass builder
    sass_options = node.data.get("_sass_options", {})
    compile_parameters = sass_options.get("compile_parameters", {})

    # spekulatio specific importer
    def importer(name, src_path_str):
        """Change sass import behavior to adapt it to Spekulatio.

        Imports are performed on the in-memory tree node structure of the
        new site and not the filetree of the original sass file.
        Also, it is possible to import from node values instead of files.
        """
        # first check if the import exists as a value
        if name in node.data:
            log.debug(f"  {node.name}: importing {name} from values.")
            return [(name, node.data[name])]

        # get the node in the node tree that should contain
        # the imported file
        import_path = Path(name)
        parts_to_parent = import_path.parent.parts
        parent_node = node.parent.get(*parts_to_parent)
        if not parent_node:
            # fall back to regular behavior if no parent in node tree
            return None

        nodes_to_check = [parent_node] + parent_node.overridden_nodes
        names_to_check = [
            f"{import_path.name}",
            f"_{import_path.name}",
            f"_{import_path.name}.scss",
            f"_{import_path.name}.sass",
            f"_{import_path.name}.css",
            f"{import_path.name}.scss",
            f"{import_path.name}.sass",
            f"{import_path.name}.css",
        ]

        for node_to_check in nodes_to_check:
            for name_to_check in names_to_check:
                full_path = node_to_check.src_path / name_to_check
                if full_path.exists():
                    full_path_str = str(full_path)
                    log.debug(f"  {node.name}: importing {name} from {full_path_str}.")
                    return [(full_path_str,)]

        # None passes control to next importer or default behavior
        return None

    # list of importers (<priority>, <function>)
    importers = [(0, importer)]

    # get content
    content = sass.compile(
        filename=str(src_path), importers=importers, **compile_parameters
    )

    # write file
    dst_path.write_text(content)
