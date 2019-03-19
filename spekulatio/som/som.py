import logging

from .node import Node
from .extractors import extractors
from .sorting import sorting_methods
from ..exceptions import SpekulatioError


class SOM:
    """The som is a tree of Node objects in which each node represents either a
    directory or a file. Each file node contains all the necessary infromation
    to render an HTML page out of it.

    The som is created by recursively traversing a root path and generating
    directory nodes out of the filesystem directories and file nodes out of:

        * RestructuredText (.rst)
        * JSON (.json)

    files.
    """
    def __init__(self, root_path):
        self.root_path = root_path
        self.map = {}

        # create the nodes and map
        self.root_node = self.create_tree(root_path)

        # calculate the data of each node using its local data and the data
        # of its ancestors
        self.set_node_data(self.root_node)

        # sort siblings
        self.sort_som_siblings(self.root_node)

        # finally, set the relationship between nodes
        self.set_som_relationships()

    def create_tree(self, path):
        """Create a site object model recursively from a directory path.

        The resulting tree will have directory and page nodes, and the metadata
        of each one will be initialized.
        """
        if not path.is_dir():
            raise SpekulatioError(f"'{path}' is not a valid directory")

        # create directory node
        node = Node(path.relative_to(self.root_path), is_dir=True)
        self.map[str(node)] = node

        # create children and get directory metadata
        duplicates = set()
        dir_data_parts = []
        for child_path in path.iterdir():

            # dir paths
            if child_path.is_dir():
                child_node = self.create_tree(child_path)
                if not child_node.skip:
                    node.add_child(child_node)

            # data/page paths
            elif child_path.suffix in extractors:

                # check duplicates
                if child_path.stem in duplicates:
                    logging.warning(f"Multiple files with the same basename: '{child_path.stem}'")
                else:
                    duplicates.add(child_path.stem)

                text = child_path.read_text()
                extractor = extractors[child_path.suffix]
                try:
                    data = extractor(text)
                except Exception as err:
                    logging.error(f"Can't process file: {child_path}. {err}")
                    continue

                if child_path.name.startswith('_'):
                    dir_data_parts.append({
                        'name': child_path.name,
                        'data': data,
                    })
                else:
                    child_node = Node(child_path.relative_to(self.root_path), is_dir=False)
                    self.map[str(child_node)] = child_node
                    child_node.local_data.update(data)
                    node.add_child(child_node)

        # set directory data
        sorted_dir_data_parts = sorted(dir_data_parts, key=lambda x: x['name'])
        for data_part in sorted_dir_data_parts:
            node.local_data.update(data_part['data'])

        return node

    def set_node_data(self, node):
        """Make data inherit from parent to children.

        In a node there are two kinds of data dictionaries:

        * local_data: data explicitly set on the node
        * data: local data merged with the inherited one

        The farder the origin of the data to a given node, the least it has
        priority over the same keys set deeper in the tree.
        """
        # inherit parent's data
        if node != self.root_node:
            node.data.update(node.parent.data)

        # merge local data
        node.data.update(node.local_data)

        # process children recursively
        for child in node.children:
            self.set_node_data(child)

    def sort_som_siblings(self, node):
        """Sort siblings in every dir node of a som."""

        # get sorting method
        sorting_method = node.data.get('_sorting_method', 'none')
        if sorting_method not in ('none', 'name', 'field', 'list'):
            msg = f"Unknown sorting method '{sorting_method}' in {node.path}. "
            msg += "Valid values: 'none', 'name', 'field', 'list'."
            raise SpekulatioError(msg)

        # get sorting direction
        sorting_direction = node.data.get('_sorting_direction', 'asc')
        if sorting_direction not in ('asc', 'desc'):
            msg = f"Wrong sorting direction '{sorting_direction}' in {node.path}. "
            msg += "Valid values: 'asc', 'desc'."
            raise SpekulatioError(msg)

        # get sorting data (for field and list sorting)
        sorting_data = node.data.get('_sorting_data')
        if not sorting_data and sorting_method in ('field', 'list'):
            msg = f"Sorting by {sorting_method} requires to set the '_sorting_data' field."
            raise SpekulatioError(msg)

        # sort the children of this node
        sorting_parameters = {
            'direction': sorting_direction,
            'data': sorting_data,
        }
        if sorting_method in sorting_methods:
            sorting_function = sorting_methods[sorting_method]
            node.children = sorting_function(node.children, **sorting_parameters)

        # sort children recursively
        for child in node.iter_dir_nodes():
            self.sort_som_siblings(child)

    def set_som_relationships(self):
        """Set the next, prev and root relationships of every node."""
        self.root_node.root = self.root_node
        prev_node = self.root_node
        for node in self.root_node.iter_nodes():
            node.root = self.root_node
            node.prev = prev_node
            prev_node.next = node
            prev_node = node

    def iter_nodes(self):
        """Yield one by one all the nodes of the som."""
        yield from self.root_node.iter_nodes()

    def list_names(self):
        """Get an ordered list of string representation of the node paths.

        Here just for testing purposes
        """
        return [str(node) for node in self.root_node.iter_nodes()]

    def __str__(self):
        return str(self.root_node)

