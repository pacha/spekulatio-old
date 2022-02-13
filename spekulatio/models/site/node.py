import logging as log
from pathlib import Path
from pprint import pprint

from jinja2.exceptions import TemplateSyntaxError

from spekulatio.exceptions import SpekulatioSkipExtraction
from spekulatio.exceptions import SpekulatioReadError
from spekulatio.exceptions import SpekulatioValueError
from spekulatio.exceptions import SpekulatioWriteError
from spekulatio.models.values import Value


class Node:
    """In-memory representation of a file or directory of the final site."""

    def __init__(self, src_root, relative_src_path, action, parent=None):

        # basic info
        self.src_root = src_root
        self.relative_src_path = relative_src_path
        self.action = action

        # depth
        self.depth = (parent.depth + 1) if parent else 0

        # relationships
        self.root = parent.root if parent else self
        self._parent = parent
        self._children = []
        self._prev = None
        self._next = None
        self._prev_sibling = None
        self._next_sibling = None

        # nodes that this node overwrites
        self.overridden_nodes = []

        # data is the effective data passed to the template.
        # It combines data from all the scopes. When a value is defined as
        # 'local' it is just included here.
        # This is the only dictionary not used to pass values down to other
        # nodes in the tree.
        self.data = {}

        # level_data applies only to the current node and its children
        # it overrides branch_data
        self.level_data = {}

        # branch_data is passed down from this node onwards
        # it's overriden by both level and local data
        self.branch_data = {}

        # default_data is passed from one node to its overridding one.
        # It's used to define values in templates that are applied to the content tree
        self.default_data = {}

        # current Spekulatio pass for this node
        # possible values: created, set_values, sort, set_relationships, render_content, build
        self.status = 'created'

    @property
    def name(self):
        return self.relative_dst_path.name

    @property
    def alias(self):
        return self.data.get("_alias")

    @property
    def url(self):
        return self.data.get("_url", self.default_url)

    @property
    def default_url(self):
        return f"{Path('/') / self.relative_dst_path}"

    @property
    def skip(self):
        """Return if this node is a non-navigating one (ie. skipped from relationships)."""
        to_be_skipped = "_skip" in self.data and self.data["_skip"]
        to_be_kept = "_skip" in self.data and self.data["_skip"] == False
        return (self.is_index and not to_be_kept) or to_be_skipped

    @property
    def user_data(self):
        return {
            key: value for key, value in self.data.items() if not key.startswith("_")
        }

    @property
    def src_path(self):
        full_path = self.src_root / self.relative_src_path
        return full_path.absolute()

    @property
    def relative_dst_path(self):
        if self.action.extension_change:
            return self.relative_src_path.with_suffix(self.action.extension_change)
        return self.relative_src_path

    @property
    def is_dir(self):
        return self.src_path.is_dir()

    @property
    def is_index(self):
        return self.name == "index.html"

    @property
    def parent(self):
        if self.is_index:
            return self._parent._parent
        return self._parent

    @property
    def prev(self):
        """Get previous node while skipping non-navigating ones."""
        if self.is_index:
            return self._parent._prev
        return self._prev

    @property
    def next(self):
        """Get next node while skipping non-navigating ones."""
        if self.is_index:
            return self._parent._next
        return self._next

    @property
    def prev_sibling(self):
        """Get previous sibling while skipping non-navigating ones."""
        if self.is_index:
            return self._parent._prev_sibling
        return self._prev_sibling

    @property
    def next_sibling(self):
        """Get next sibling while skipping non-navigating ones."""
        if self.is_index:
            return self._parent._next_sibling
        return self._next_sibling

    @property
    def children(self):
        """Return children of this node except for non-navigating ones."""
        return [child for child in self._children if not child.skip]

    @property
    def title(self):
        try:
            return self.data["_title"]
        except SpekulatioReadError:
            raise SpekulatioReadError(
                f"The title of node '{self.relative_dst_path}' is being referenced "
                "before it has been processed. If you want to include a reference to it inside "
                "the content of another node (eg. {{{{ _node.next_sibling.title }}}}), "
                "then explicitely define the '_title' value in the front matter of "
                "the target node instead of inferring it from the first header of "
                "its content."
            )

    @property
    def content(self):
        return self._get_extracted_value("_content", "")

    @property
    def src_text(self):
        return self._get_extracted_value("_src_text", "")

    @property
    def toc(self):
        return self._get_extracted_value("_toc", [])

    def _get_extracted_value(self, key, default_value):
        try:
            return self.data[key]
        except KeyError:
            if self.status not in ["render_content", "build"]:
                attribute_name = key[1:]
                raise SpekulatioReadError(
                    f"Can't read attribute '{attribute_name}' of node '{self.relative_dst_path}' because "
                    f"the content of that node hasn't been processed yet. {self.status}"
                )
            else:
                return default_value

    def get(self, *children_names):
        current_node = self
        for child_name in children_names:
            if child_name in ["", "."]:
                continue
            elif child_name == "..":
                current_node = current_node._parent
            else:
                current_node = current_node.get_child(child_name)
                if not current_node:
                    return None
        return current_node

    def get_child(self, child_name):
        """Get a child given its name."""
        for child in self._children:
            if child_name == child.name:
                return child
        return None

    def get_dst_path(self, output_path):
        full_path = output_path / self.relative_dst_path
        return full_path.absolute()

    def get_ancestors(self):
        yield self
        current_node = self
        while current_node._parent:
            yield current_node._parent
            current_node = current_node._parent

    def get_ancestor(self, depth):
        for node in self.get_ancestors():
            if node.depth == depth:
                return node
        raise SpekulatioWriteError(
            f"Ancestor of '{self.url}' at depth '{depth}' not found."
        )

    def is_descendant_of(self, potential_ancestor):
        for node in self.get_ancestors():
            if node == potential_ancestor:
                return True
        return False

    def traverse(self):
        yield self
        for child in self.children:
            yield from child.traverse()

    def traverse_all(self):
        yield self
        for child in self._children:
            yield from child.traverse_all()

    def print_data(self):
        """Print node data dicts (for debugging purposes)."""
        print("--branch_data:")
        pprint(self.branch_data)
        print("--level_data:")
        pprint(self.level_data)
        print("--data:")
        pprint(self.data)

    def __repr__(self):
        return f"<Node: {self.name}>"

    def __str__(self):
        indent = "│   " * (self.depth - 1)
        tail = "/" if self.is_dir else ""
        return f"{indent}├── {self.name}{tail}"

    def set_values(self, site):
        """Take user values and store then in the node.

        sources for data:

        - Node overriding: default_data
        - Inheritance:   branch_data, local_data (from level_data)
        - Node values:   default_data, branch_data, level_data, local_data
        """

        # set new status
        self.status = 'set_values'

        # set values from parent
        if self._parent:
            self.branch_data.update(self._parent.branch_data)
            self.data.update(self._parent.branch_data)
            self.data.update(self._parent.level_data)

        # get values from overriden nodes
        for overridden_node in self.overridden_nodes:

            # extract values from the node
            try:
                overridden_values = overridden_node.extract_node_values(site)
            except SpekulatioSkipExtraction:
                continue

            self._update_data(overridden_values["default"], self.branch_data)
            self._update_data(overridden_values["default"], self.data)

        # get values defined in this node
        try:
            values = self.extract_node_values(site)
        except SpekulatioSkipExtraction:
            return

        # set own default values (they go directly to branch data)
        self._update_data(values["default"], self.branch_data)
        self._update_data(values["default"], self.data)

        # set branch values
        self._update_data(values["branch"], self.branch_data)
        self._update_data(values["branch"], self.data)

        # level values
        self._update_data(values["level"], self.level_data)
        self._update_data(values["level"], self.data)

        # local values
        self._update_data(values["local"], self.data)

        # guarantee that there's always a url
        if "_url" not in self.data or not self.data["_url"]:
            self.data["_url"] = self.default_url

    def extract_node_values(self, site):
        """Extract values defined in this node."""
        # get values from _values.yaml file or frontmatter
        data_dict = self.action.extract_values(self, site)

        # convert raw values to value objects
        try:
            values = Value.get_values_from_dict(data_dict)
        except Exception as err:
            raise SpekulatioReadError(f"Wrong values at '{self.src_path}': {err}")

        return values

    @staticmethod
    def _update_data(values, data):
        """Update a given data dictionary with the provided values.

        The operation of the values is taken into account. This method should be
        called for each scope independently.
        """
        for value in values:
            if value.operation == "replace":
                data[value.name] = value.value
            elif value.operation in ("merge", "append"):
                try:
                    old_value = data[value.name]
                except KeyError:
                    data[value.name] = value.value
                else:
                    target_type = dict if value.operation == "merge" else list
                    if not isinstance(old_value, target_type):
                        raise SpekulatioValueError(
                            f"Invalid {value.operation} operation for '{value.name}'. "
                            "Destination value not of type {target_type}."
                        )
                    if value.operation == "merge":
                        new_dict = {}
                        new_dict.update(old_value)
                        new_dict.update(value.value)
                        data[value.name] = new_dict
                    else:
                        data[value.name] = old_value + value.value
            elif value.operation == "delete":
                try:
                    del data[value.name]
                except KeyError:
                    log.warning(
                        f"Invalid deleting operation for '{value.name}': "
                        f"value doesn't exist."
                    )

    def sort(self):
        """Sort nodes recursively.

        Each node sorts its children according to the list of names provided
        by the user:

        * If there's no list, children nodes are ordered alphabetically.
        * If there's a list and contains all the names of the children nodes,
          children nodes are ordered according to it.
        * If the list is larger than the number of children or contains any
          name that doesn't match any of the children an error is raised.
        * If the list is shorter than the number of children, the extra children
          will be added at the end sorted alphabetically.
        """

        # set new status
        self.status = 'sort'

        # sort only directories
        if not self.is_dir:
            return

        # get sorting options
        try:
            sorting_field = self.data["_sort_options"]["field"]
        except KeyError:
            sorting_field = "name"
        try:
            sorting_reverse = self.data["_sort_options"]["reverse"]
        except KeyError:
            sorting_reverse = False

        # get user's list of sorting values
        sorting_values = self.data.get("_sort", [])

        # create a map of child nodes for fast access
        try:
            children_map = {
                getattr(child, sorting_field): child for child in self._children
            }
        except AttributeError:
            raise SpekulatioValueError(
                f"{self.src_path}: invalid sorting field '{sorting_field}'."
            )

        # split sorting values at '*' (if not present, assume it is the last element)
        try:
            sink_position = sorting_values.index("*")
        except ValueError:
            sink_position = len(sorting_values)

        # sort from the beginning to the sink position
        top_values = sorting_values[:sink_position]
        top_sorted_nodes = self._sort_with_values(top_values, children_map)

        # sort from the sink position to the end
        bottom_values = sorting_values[(sink_position + 1) :]
        bottom_sorted_nodes = self._sort_with_values(bottom_values, children_map)

        # sort all remaining nodes alphabetically and assign them to the sink
        # (this is the complete set of children if no user list was provided)
        sorted_sink_values = sorted(children_map.keys(), reverse=sorting_reverse)
        sink_sorted_nodes = []
        for value in sorted_sink_values:
            sink_sorted_nodes.append(children_map[value])

        # use the new list as the children one
        self._children = top_sorted_nodes + sink_sorted_nodes + bottom_sorted_nodes

        # execute recursively
        for child in self._children:
            child.sort()

    def _sort_with_values(self, values, node_map):
        """Return a list of nodes from node_map according to the order in ``values``.

        Sorted nodes are removed from ``node_map``.

        :param values: a list of one of the attributes of Node ['v2', 'v1', ...]
        :param node_map: a dict of the form {'v1': node1, 'v2': node2, ...
        :return: a list of the form [node2, node1, ...]
        """
        sorted_nodes = []
        for value in values:

            # get node
            try:
                node_key = value
                node = node_map[node_key]
            except KeyError:
                # try to append '.html' if node not found in first try
                try:
                    node_key = value + ".html"
                    node = node_map[node_key]
                except KeyError:
                    raise SpekulatioValueError(
                        f"{self.src_path}: can't sort '{value}'. There's no node with that name "
                        "or it is an empty directory."
                    )

            # add it to sorted nodes
            sorted_nodes.append(node)

            # remove it from the map
            del node_map[node_key]

        return sorted_nodes

    def render_content(self, site):
        """Extract values derived from the content of the node by parsing and rendering it.

        The content values are:

            * _content: Markdown, RestructuredText or HTML already rendered and converted into HTML.
            * _title: Top level header of the content.
            * _toc: Nested structure with the titles of the content in the format:

                [{'level': 1, 'id': 'slug', 'name': 'Main title', 'children': [...]}]
        """

        # set new status
        self.status = 'render_content'

        # extract content
        try:
            content_values = self.action.extract_content(self, site)
        except TemplateSyntaxError as err:
            raise SpekulatioReadError(f"Jinja syntax error at {self.src_path}: {err}")
        except Exception as err:
            raise SpekulatioReadError(f"Can't render {self.src_path}: {err}")
        self.data.update(content_values)

        # guarantee that there's always a title
        if "_title" not in self.data or self.data["_title"] is None:
            try:
                self.data["_title"] = self.data["_toc"][0]["name"]
            except (KeyError, IndexError):
                self.data["_title"] = self.url

    def build(self, output_path, only_modified, site):
        """Persist this node in the destination location."""

        # set new status
        self.status = 'build'

        # get paths
        src_path = self.src_path
        dst_path = self.get_dst_path(output_path)

        # check if it is necessary to generate the new file
        if only_modified:

            # check age of destination file
            if dst_path.is_file():
                dst_timestamp = dst_path.stat().st_mtime
                src_timestamp = src_path.stat().st_mtime
                if dst_timestamp >= src_timestamp:
                    log.debug(
                        f" [skipping] {self.relative_dst_path}. Destination newer than source."
                    )
                    return

        # build node
        log.debug(
            f" [writing] {self.relative_dst_path} ({self.action.__name__.split('.')[-1]})"
        )
        self.action.build(src_path, dst_path, self, site)

        # build children
        for child in self._children:
            child.build(output_path, only_modified, site)
