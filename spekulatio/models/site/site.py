import re
import json
import logging as log
from pathlib import Path
from datetime import datetime

import jinja2

from spekulatio.models.values import Value
from spekulatio.models.actions import create_dir
from spekulatio.models.actions import virtual_node
from spekulatio.models.filetrees import get_filetype
from spekulatio.exceptions import SpekulatioReadError
from spekulatio.exceptions import SpekulatioBuildError
from spekulatio.exceptions import SpekulatioInternalError

from .node import Node


class Site:
    """The site, modeled as a tree of Nodes.

    The process of getting a site prepared requires:

        * Multiple calls to 'from_directory' to add as many filetrees as needed.
          After that, the node tree already exists and the data dictionaries
          are initialized.
        * One call to 'set_relationships' to sort the nodes at each level and
          set the links between them. This has to be done after the previous
          'from_directory' calls as the sorting configuration is obtained from
          the node values.
        * One call to 'build' to create the site.
    """

    def __init__(self, build_path, only_modified):

        # building parameters
        self.build_path = build_path
        self.only_modified = only_modified
        self.template_dirs = []

        # node structure
        self.root = None
        self.nodes = {}
        self.aliases = {}

    def display_tree(self):
        node_iterator = self.root.traverse()

        # discard root and just print it as a slash
        next(node_iterator)
        log.debug("/")

        # print each node
        for node in node_iterator:
            log.debug(f"{node}")

    def from_directory(self, directory_path, filetree_conf):
        # use as jinja template directory if configured as such
        if filetree_conf.template_dir:
            self.template_dirs.insert(0, directory_path)

        # create the node tree recursively
        self.root = self._from_path(
            directory_path, directory_path, filetree_conf, parent=None
        )

    def _from_path(self, src_root, path, filetree_conf, parent):
        """Recursively traverse a directory and add its nodes to the site tree.

        :param src_root: absolute path to the directory being added
        :param path: path currently being processed during the recursion
        :param filetree_conf: map of actions to apply in this directory
        :param parent: parent node to attach the new node to
        """
        # get relative source path
        relative_src_path = path.relative_to(src_root)

        # check if path has to be included
        for ignore_pattern in filetree_conf.ignore_patterns:
            if re.match(ignore_pattern, path.name):
                log.debug(f" [skipping] {relative_src_path}")
                return None

        # get action for this kind of path
        default_action = filetree_conf.default_action
        filetype = get_filetype(path)
        action = filetree_conf.actions.get(filetype, default_action)

        # create node
        node = Node(src_root, relative_src_path, action, parent)

        # check if there's an existing node at the same location
        old_node = self.nodes.get(node.default_url)
        if old_node:

            # check that the ouput is not ambiguous
            same_src_root = node.src_root == old_node.src_root
            different_relative_path = (
                node.relative_src_path != old_node.relative_src_path
            )
            if same_src_root and different_relative_path:
                raise SpekulatioReadError(
                    f"Ambiguous input both: '{node.relative_src_path}' and "
                    f"'{old_node.relative_src_path}' at '{node.src_root}' can potentially "
                    f"generate the same output file '{node.relative_dst_path}'. "
                    "Add only one input file for each associated output file."
                )

            # inherit list of overwritten nodes and add new entry
            node.overridden_nodes = old_node.overridden_nodes
            node.overridden_nodes.append(old_node)

            # inherit children
            node._children = old_node._children
            for child in node._children:
                child._parent = node

        # process children
        is_dir = path.is_dir()
        has_children = False
        if is_dir:
            for child_src_path in path.iterdir():
                child_node = self._from_path(
                    src_root, child_src_path, filetree_conf, parent=node
                )
                has_children = child_node or has_children

        # register new node
        # (directories without children won't be registered)
        is_root = not parent
        register = not is_dir or has_children or is_root
        if not register:
            return None

        self.nodes[node.default_url] = node
        if parent:
            # remove overwritten node from parent's children list
            if old_node:
                if old_node.default_url != "/":
                    log.debug(
                        f" [node overwritten] {relative_src_path} overwrites previous node"
                    )
                parent._children.remove(old_node)

            # add new node
            parent._children.append(node)

        if node.action != virtual_node:
            log.debug(f" [new node] {relative_src_path} > {node.default_url}")
        else:
            log.debug(f" [new node] {relative_src_path} (no output: virtual node)")

        return node

    def set_values(self):
        """Set values for nodes recursively."""
        # check if site has been initialized
        if not self.root:
            raise SpekulatioReadError(
                "Site not initialized yet. "
                "Use Site.from_directory(...) to add content to it."
            )

        # process values
        for node in self.root.traverse():
            node.set_values()

    def sort(self):
        """Sort nodes recursively."""
        # check if site has been initialized
        if not self.root:
            raise SpekulatioReadError(
                "Site not initialized yet. "
                "Use Site.from_directory(...) to add content to it."
            )
        self.root.sort()

    def set_relationships(self):
        """Set links between nodes.

        Index nodes and nodes marked with '_skip' are not included:

            * Index nodes have the same relationships as their directory parents
            * Skipped nodes have their prev/next links set to None
        """
        # check if site has been initialized
        if not self.root:
            raise SpekulatioReadError(
                "Site not initialized yet. "
                "Use Site.from_directory(...) to add content to it."
            )

        # traverse nodes setting relationships as we go
        prev_node = None
        for node in self.root.traverse():

            # add to aliases
            if node.alias:
                self.aliases[node.alias] = node

            # skip if necessary
            if node.skip:
                continue

            # set prev/next
            node._prev = prev_node
            if prev_node:
                prev_node._next = node
            prev_node = node

            # set siblings
            previous_sibling = None
            for child in node._children:
                if child.skip:
                    continue
                child._prev_sibling = previous_sibling
                if previous_sibling:
                    previous_sibling._next_sibling = child
                previous_sibling = child

    def build(self):
        """Create files in the destination location."""
        # check if site has been initialized
        if not self.root:
            raise SpekulatioReadError(
                "Site not initialized yet. "
                "Use Site.from_directory(...) to add content to it."
            )

        # check if there's content to build
        if not self.root._children:
            log.warn(
                "Your site is empty. "
                "Did you provide the correct directories to build it?"
            )
            return

        # get building environment
        build_env = self._get_build_env()

        # build nodes recursively
        self.root.build(self.build_path, self.only_modified, build_env)

    def _get_build_env(self):
        build_env = {
            "jinja_env": self._get_jinja_env(),
        }
        return build_env

    def _get_jinja_env(self):
        """Initialize templating environment."""

        def get_node(url=None, alias=None):
            """Get node using its url or its alias."""
            if url:
                try:
                    return self.nodes[url]
                except KeyError:
                    raise SpekulatioBuildError(f"Can't find node with url={url}")
            if alias:
                try:
                    return self.aliases[alias]
                except KeyError:
                    raise SpekulatioBuildError(f"Can't find node with alias={alias}")
            raise SpekulatioBuildError(
                f"'get_node()' must be called passing either an url or an alias."
            )

        def print_as_json(dictionary):
            return json.dumps(dictionary, indent=2)

        def now_as(format):
            """Returns current date/time as a string.

            :param format: strftime() style string
            """
            now = datetime.now()
            return now.strftime(format)

        template_dirs = [
            str(template_dir.absolute()) for template_dir in self.template_dirs
        ]
        loader = jinja2.FileSystemLoader(template_dirs, followlinks=True)
        jinja_env = jinja2.Environment(loader=loader)

        jinja_env.globals.update(get_node=get_node)
        jinja_env.globals.update(print_as_json=print_as_json)
        jinja_env.globals.update(now_as=now_as)

        return jinja_env
