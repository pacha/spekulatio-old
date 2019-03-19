
from collections import OrderedDict

class Node:
    """Base class of all the nodes in a som."""

    def __init__(self, path, is_dir):
        self.path = path
        self.is_dir = is_dir
        self.local_data = OrderedDict()
        self.data = OrderedDict()

        # relationships
        self.parent = None
        self.next = None
        self.prev = None
        self.root = None
        self.children = []

    @property
    def skip(self):
        return self.is_dir and not bool(self.children)

    def iter_nodes(self):
        """Traverse tree from this node."""
        for node in self.children:
            yield node
            if node.is_dir:
                yield from node.iter_nodes()

    def iter_dir_nodes(self):
        """Return only children nodes that are directories."""
        for child in self.children:
            if child.is_dir:
                yield child

    def add_child(self, node):
        """Set parent/child relationship between this and the passed node."""
        self.children.append(node)
        node.parent = self

    def __str__(self):
        return str(self.path)

    def __repr__(self):
        return f'<{self.__class__}:{self.path}>'

