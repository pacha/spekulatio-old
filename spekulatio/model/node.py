import logging as log
from pathlib import Path

import yaml

from spekulatio.exceptions import SpekulatioReadError
from spekulatio.exceptions import SpekulatioValueError
from .frontmatter import parse_frontmatter
from .value import Value


class Node:
    """A file or directory of the generated site."""

    def __init__(self):

        # basic info
        self.src_root = None
        self.relative_src_path = None
        self.relative_dst_path = None
        self.action = None
        self.filetype = None

        # relationships
        self.parent = None
        self.children = []
        self.root = None
        self.next = None
        self.prev = None
        self.next_sibling = None
        self.prev_sibling = None

        # depth
        self.depth = None

        # content
        self.text = None

        # effective combination of the data in all scopes
        self.data = {}

        # local_data is defined in the front-matter and is never passed down
        # it overrides all the rest
        self.local_data = {}

        # level_data is passed down only to inmediate children
        # it overrides branch_data
        self.level_data = {}

        # branch_data is passed down from this point onwards
        # it's overriden by both level and local data
        self.branch_data = {}

    def set_basic_info(
        self, src_root, relative_src_path, relative_dst_path, filetype, action
    ):
        self.src_root = src_root
        self.relative_src_path = relative_src_path
        self.relative_dst_path = relative_dst_path
        self.filetype = filetype
        self.action = action

    def setup(self, depth=0):
        """Load data, sort childern and set relationships from this node on."""
        log.debug(f" [setup] {self.relative_dst_path}")
        self.depth = depth
        self._set_data()
        self._sort_children()
        self._set_relationships()
        for child in self.children:
            child.setup(depth=depth + 1)

    def _set_data(self):
        """Set the contents of the node.

        The following fields are initialized:

        * self.text
        * self.data
        * self.level_data
        * self.branch_data
        """
        # inherit data from parent
        if self.parent:
            self.branch_data.update(self.parent.branch_data)
            self.data.update(self.parent.branch_data)
            self.data.update(self.parent.level_data)

        # read values from disk
        text, values = self._get_text_and_values()
        self.text = text
        for value in values:
            log.debug(f"{value}")

        #   (parent)        (child)
        # branch data -> branch data
        #             -> data
        # level data  -> data
        #                if dir:
        #                   branch scope > branch_data
        #                   level scope  > level_data
        #                   frontmatter -> data
        #                else:
        #                   frontmatter -> data

    def _get_text_and_values(self):
        if self.filetype == "directory":
            text, values = self._read_directory_node()
        elif self.filetype in ("md", "rst"):
            text, values = self._read_frontmatter_node()
        elif self.filetype in ("json", "yaml"):
            text, values = self._read_datatext_node()
        else:
            text, values = None, []
        return text, values

    def _read_directory_node(self):
        values_path = self.src_path / "_values.yaml"

        # read content
        try:
            values_content = values_path.read_text()
        except FileNotFoundError:
            log.debug(f" [{self.src_path}] No values file found.")
            return None, []

        # parse yaml
        try:
            raw_values = yaml.safe_load(values_content)
        except Exception as err:
            raise SpekulatioReadError(f"Can't parse {values_path}: {err}")

        text = None
        try:
            values = [Value(key, raw_value) for key, raw_value in raw_values.items()]
        except SpekulatioValueError as err:
            raise SpekulatioReadError(f"Wrong value at {values_path}: {err}")
        return text, values

    def _read_frontmatter_node(self):
        # read content
        try:
            raw_content = self.src_path.read_text()
        except FileNotFoundError:
            raise SpekulatioReadError(f"Can't read {self.src_path}")

        # parse frontmatter
        try:
            text, raw_values = parse_frontmatter(raw_content)
        except SpekulatioFrontmatterError as err:
            raise SpekulatioReadError(
                f"Can't parse frontmatter at {self.src_path}: {err}"
            )

        # convert to values objects
        try:
            values = [Value(key, raw_value) for key, raw_value in raw_values.items()]
        except SpekulatioValueError as err:
            raise SpekulatioReadError(f"Wrong value at {self.src_path}: {err}")
        return text, values

    def _read_datatext_node(self):
        # read content
        try:
            text = self.src_path.read_text()
        except FileNotFoundError:
            raise SpekulatioReadError(f"Can't read {self.src_path}")
        values = []
        return text, values

    def _sort_children(self):
        pass

    def _set_relationships(self):
        pass

    @property
    def name(self):
        return self.relative_dst_path.name

    @property
    def url_path(self):
        return f"{Path('/') / self.relative_dst_path}"

    @property
    def src_path(self):
        return self.src_root / self.relative_src_path

    def get_build_path(self, build_dir):
        return build_dir / self.relative_dst_path

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def traverse(self):
        yield self
        for child in self.children:
            yield from child.traverse()

    def __str__(self):
        indent = "│   " * (self.depth - 1)
        prefix = f"{indent}├── "
        marker = "/" if self.filetype == "directory" else ""
        return f"{prefix}{self.name}{marker}"
