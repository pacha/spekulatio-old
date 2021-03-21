import logging as log
from pathlib import Path

from .node import Node
from .actions import create_dir


class Site:
    """The site, modeled as a tree of Nodes."""

    def __init__(self, build_path, only_modified):
        self.build_path = build_path
        self.only_modified = only_modified
        self.root = Node()
        self.root.set_basic_info(
            None, Path("."), Path("."), "directory", action=create_dir
        )

        # path cache (url_path: node)
        self.nodes = {
            "/": self.root,
        }

    def from_directory(self, directory_path, actionmap):
        self._from_path(directory_path, directory_path, actionmap, parent=None)

    def _from_path(self, src_root, path, actionmap, parent):
        """Recursively traverse a directory and add its nodes to the site tree.

        :param src_root: absolute path to the directory being added
        :param path: path currently being processed during the recursion
        :param actiomap: map of actions for this directory
        :param parent: parent node to attach the new node to
        """

        if path.is_dir():
            self._from_dir(src_root, path, actionmap, parent)
        else:
            self._from_file(src_root, path, actionmap, parent)

    def _from_file(self, src_root, path, actionmap, parent):

        # get action and relative paths
        filetype, action, extension_change = actionmap.match(path.name)
        relative_src_path = path.relative_to(src_root)
        if extension_change:
            relative_dst_path = relative_src_path.with_suffix(extension_change)
        else:
            relative_dst_path = relative_src_path

        # log action to perform
        if not action:
            log.debug(f" [action: ignore] {relative_src_path}")
            return
        log.debug(
            f" [action: {action.__name__}] {relative_src_path} -> {relative_dst_path}"
        )

        # get or create node
        url_path = str(Path("/") / relative_dst_path)
        try:
            node = self.nodes[url_path]
            node.set_basic_info(
                src_root, relative_src_path, relative_dst_path, filetype, action
            )
        except KeyError:
            node = Node()
            node.set_basic_info(
                src_root, relative_src_path, relative_dst_path, filetype, action
            )
            parent.add_child(node)

    def _from_dir(self, src_root, path, actionmap, parent):

        action = create_dir
        relative_src_path = path.relative_to(src_root)
        relative_dst_path = relative_src_path

        # get or create node
        url_path = str(Path("/") / relative_dst_path)
        try:
            node = self.nodes[url_path]
            node.set_basic_info(
                src_root, relative_src_path, relative_dst_path, "directory", action
            )
            already_appended = True
        except KeyError:
            node = Node()
            node.set_basic_info(
                src_root, relative_src_path, relative_dst_path, "directory", action
            )
            already_appended = False

        # process children
        for child_src_path in path.iterdir():
            self._from_path(src_root, child_src_path, actionmap, node)

        # only add a directory if contains children
        if not already_appended and node.children:
            parent.add_child(node)

    def setup_nodes(self):
        """Read values, sort nodes and set relationships."""
        self.root.setup()

    def build(self):
        pass

    def display_tree(self):
        node_iterator = self.root.traverse()

        # discard root and just print it as a slash
        next(node_iterator)
        log.debug("/")

        # print each node
        for node in node_iterator:
            log.debug(f"{node}")
