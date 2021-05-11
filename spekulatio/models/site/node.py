import logging as log
from pathlib import Path
from pprint import pprint

from jinja2.exceptions import TemplateNotFound

from spekulatio.exceptions import SpekulatioReadError
from spekulatio.exceptions import SpekulatioValueError
from spekulatio.models.values import Value
from spekulatio.models.filetrees import get_category

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
        self.parent = parent
        self.children = []
        self.root = parent.root if parent else self
        self.next = None
        self.prev = None
        self.next_sibling = None
        self.prev_sibling = None

        # local_data is the effective data passed to the template.
        # When a value is defined as 'local' is not passed down to any other node
        # and overrides any other previous definition
        self.local_data = {}

        # level_data applies only to the current node and its children
        # it overrides branch_data
        self.level_data = {}

        # branch_data is passed down from this node onwards
        # it's overriden by both level and local data
        self.branch_data = {}

    @property
    def name(self):
        return self.relative_dst_path.name

    @property
    def data(self):
        return self.local_data

    @property
    def user_data(self):
        return {key: value for key, value in self.local_data.items() if not key.startswith('_')}

    @property
    def category(self):
        return get_category(self.relative_dst_path)

    @property
    def url(self):
        return f"{Path('/') / self.relative_dst_path}"

    @property
    def src_path(self):
        full_path = self.src_root / self.relative_src_path
        return full_path.absolute()

    @property
    def is_dir(self):
        return self.src_path.is_dir()

    @property
    def relative_dst_path(self):
        if self.action.extension_change:
            return self.relative_src_path.with_suffix(self.action.extension_change)
        return self.relative_src_path

    def get_dst_path(self, build_path):
        full_path = build_path / self.relative_dst_path
        return full_path.absolute()

    def traverse(self):
        yield self
        for child in self.children:
            yield from child.traverse()

    def print_data(self):
        """Print node data dicts (for debugging purposes)."""
        print("--branch_data:")
        pprint(self.branch_data)
        print("--level_data:")
        pprint(self.level_data)
        print("--local_data:")
        pprint(self.local_data)

    def __repr__(self):
        return f"<Node: {self.name}>"

    def __str__(self):
        indent = "│   " * (self.depth - 1)
        tail = '/' if self.is_dir else ''
        return f"{indent}├── {self.name}{tail}"

    def set_values(self):
        """Take user values and store then in the node."""

        # get values for this node (from a _values.yaml file or a frontmatter)
        data_dict = self.action.extract(self)

        # convert raw values to value objects
        try:
            values = Value.get_values_from_dict(data_dict)
        except Exception as err:
            raise SpekulatioReadError(f"Wrong values at '{self.src_path}': {err}")

        # branch values
        if self.parent:
            self.branch_data.update(self.parent.branch_data)
        self._update_data(values['branch'], self.branch_data)

        # level values
        self.level_data.update(self.branch_data)
        self._update_data(values['level'], self.level_data)

        # local values
        self.local_data.update(self.level_data)
        if self.parent:
            self.local_data.update(self.parent.level_data)
        self._update_data(values['local'], self.local_data)

    @staticmethod
    def _update_data(values, data):
        """Update a given data dictionary with the provided values.

        The operation of the values is taken into account. This method should be
        called for each scope independently.
        """
        for value in values:
            if value.operation == 'replace':
                data[value.name] = value.value
            elif value.operation in ('merge', 'append'):
                try:
                    old_value = data[value.name]
                except KeyError:
                    data[value.name] = value.value
                else:
                    target_type = dict if value.operation == 'merge' else list
                    if not isinstance(old_value, target_type):
                        raise SpekulatioValueError(
                            f"Invalid {value.operation} operation for '{value.name}'. "
                            "Destination value not of type {target_type}."
                        )
                    if value.operation == 'merge':
                        old_value.update(value.value)
                    else:
                        old_value.extend(value.value)
            elif value.operation == 'delete':
                try:
                    del data[value.name]
                except KeyError:
                    pass

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
        # sort only directories
        if not self.is_dir:
            return

        # get sorting options
        try:
            sorting_field = self.local_data['_sort_options']['field']
            sorting_reverse = self.local_data['_sort_options']['reverse']
        except KeyError:
            raise SpekulatioValueError(
                f"{self.src_path}: incomplete sorting options. "
                "You need to specify both 'field' and 'reverse' values."
            )

        # get user's list of sorting values
        sorting_values = self.local_data.get('_sort', [])

        # create a map of child nodes for fast access
        try:
            children_map = {getattr(child, sorting_field): child for child in self.children}
        except AttributeError:
            raise SpekulatioValueError(
                f"{self.src_path}: invalid sorting field '{sorting_field}'."
            )

        # split sorting values at '*' (if not present, assume it is the last element)
        try:
            sink_position = sorting_values.index('*')
        except ValueError:
            sink_position = len(sorting_values)

        # sort from the beginning to the sink position
        top_values = sorting_values[:sink_position]
        top_sorted_nodes = self._sort_with_values(top_values, children_map)

        # sort from the sink position to the end
        bottom_values = sorting_values[(sink_position + 1):]
        bottom_sorted_nodes = self._sort_with_values(bottom_values, children_map)

        # sort all remaining nodes alphabetically and assign them to the sink
        # (this is the complete set of children if no user list was provided)
        sorted_sink_values = sorted(children_map.keys(), reverse=sorting_reverse)
        sink_sorted_nodes = []
        for value in sorted_sink_values:
            sink_sorted_nodes.append(children_map[value])

        # use the new list as the children one
        self.children = top_sorted_nodes + sink_sorted_nodes + bottom_sorted_nodes

        # execute recursively
        for child in self.children:
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

            # get child
            try:
                node = node_map[value]
            except KeyError:
                raise SpekulatioValueError(
                    f"{self.src_path}: can't sort {value}. There's no node with that name."
                )

            # add it to sorted nodes
            sorted_nodes.append(node)

            # remove it from the map
            del node_map[value]

        return sorted_nodes


    def build(self, build_path, only_modified, build_env):
        """Persist this node in the destination location."""

        # get paths
        src_path = self.src_path
        dst_path = self.get_dst_path(build_path)

        # check if it is necessary to generate the new file
        if only_modified:

            # check age of destination file
            if dst_path.is_file():
                dst_timestamp = dst_path.stat().st_mtime
                src_timestamp = src_path.stat().st_mtime
                if dst_timestamp >= src_timestamp:
                    log.debug(f" [skipping] {self.relative_dst_path}. Destination newer than source.")
                    return

        # build node
        log.debug(f" [build] {self.relative_dst_path} (action: {self.action.__name__})")
        self.action.build(src_path, dst_path, self, **build_env)


        # build children
        for child in self.children:
            child.build(build_path, only_modified, build_env)

    def render_html(self, jinja_env):

        # get parameters from configuration
        try:
            default_template = self.local_data['_jinja_options']['default_template']
        except KeyError:
            raise SpekulatioValueError(
                f"{self.src_path}: missing 'default_template' in '_jinja_options'"
            )

        # get template
        template_name = self.local_data.get("_template", default_template)
        try:
            template = jinja_env.get_template(template_name)
        except TemplateNotFound:
            raise SpekulatioValueError(
                f"{self.src_path}: template '{template_name}' not found."
            )

        # write content
        content = template.render(_node=self, **self.local_data)

        return content

