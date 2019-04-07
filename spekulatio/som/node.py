
from collections import OrderedDict

class Node:
    """Base class of all the nodes in a som."""

    def __init__(self, path, is_dir):
        self.path = path
        self.is_dir = is_dir
        self.raw_data = OrderedDict()
        self.local_data = OrderedDict()
        self.global_data = OrderedDict()
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

    @property
    def url(self):
        # if set explicitly, return the value provided by the user
        manually_set_url = self.data.get('_url')
        if manually_set_url:
            return manually_set_url

        # calculate the relative destination path/url
        relative_path = self.path.relative_to(self.root.path)
        if self.is_dir:
            html_path = relative_path / 'index.html'
        else:
            html_path = relative_path.with_suffix('.html')
        relative_url = f"/{'/'.join(html_path.parts)}"
        return relative_url


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

