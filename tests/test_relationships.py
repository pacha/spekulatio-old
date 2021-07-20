from pathlib import Path

import pytest

from spekulatio.models import Site
from spekulatio.models.input_dirs import InputDir
from spekulatio.paths import default_input_dir_path
from spekulatio.exceptions import SpekulatioReadError


def test_root(fixtures_path):

    # source files path
    content_path = fixtures_path / "relationships" / "root" / "content"
    content_dir = InputDir(content_path, "site_content")

    site = Site(output_path=None, only_modified=False)
    site.from_directory(content_dir)

    # check all nodes
    dir1 = site.nodes["/dir1"]
    assert dir1.root == site.root

    foo = site.nodes["/foo.html"]
    assert foo.root == site.root

    dir2 = site.nodes["/dir1/dir2"]
    assert dir2.root == site.root

    bar = site.nodes["/dir1/bar.html"]
    assert bar.root == site.root

    baz = site.nodes["/dir1/dir2/baz.js"]
    assert baz.root == site.root


def test_prev_next(fixtures_path):

    # source files path
    content_path = fixtures_path / "relationships" / "prev-next" / "content"
    content_dir = InputDir(content_path, "site_content")

    site = Site(output_path=None, only_modified=False)
    site.from_directory(content_dir)
    site.set_values()
    site.sort()
    site.set_relationships()

    # check all nodes
    foo = site.nodes["/foo.html"]
    dir1 = site.nodes["/dir1"]

    dir2 = site.nodes["/dir1/dir2"]

    bak = site.nodes["/dir1/dir2/bak.html"]
    bat = site.nodes["/dir1/dir2/bat.html"]

    baz = site.nodes["/dir1/baz.html"]

    bar = site.nodes["/bar.html"]

    assert site.root.next == foo
    assert foo.next == dir1
    assert dir1.next == dir2
    assert dir2.next == bak
    assert bak.next == bat
    assert bat.next == baz
    assert baz.next == bar


def test_siblings(fixtures_path):

    # source files path
    content_path = fixtures_path / "relationships" / "siblings" / "content"
    content_dir = InputDir(content_path, "site_content")

    site = Site(output_path=None, only_modified=False)
    site.from_directory(content_dir)
    site.set_values()
    site.sort()
    site.set_relationships()

    # check all nodes
    foo = site.nodes["/foo.html"]
    dir1 = site.nodes["/dir1"]
    bar = site.nodes["/bar.html"]

    dir2 = site.nodes["/dir1/dir2"]
    baz = site.nodes["/dir1/baz.html"]

    bak = site.nodes["/dir1/dir2/bak.html"]
    bat = site.nodes["/dir1/dir2/bat.html"]

    assert site.root.next_sibling is None
    assert site.root.prev_sibling is None

    assert foo.prev_sibling is None
    assert foo.next_sibling is dir1
    assert dir1.prev_sibling is foo
    assert dir1.next_sibling is bar
    assert bar.prev_sibling is dir1
    assert bar.next_sibling is None

    assert dir2.prev_sibling is None
    assert dir2.next_sibling is baz
    assert baz.prev_sibling is dir2
    assert baz.next_sibling is None

    assert bak.prev_sibling is None
    assert bak.next_sibling is bat
    assert bat.prev_sibling is bak
    assert bat.next_sibling is None


def test_get_method(fixtures_path):

    # input dirs
    templates_path = fixtures_path / "relationships" / "get-method" / "templates"
    templates_dir = InputDir(templates_path, "site_templates")
    content_path = fixtures_path / "relationships" / "get-method" / "content"
    content_dir = InputDir(content_path, "site_content")

    # build site
    site = Site(output_path=None, only_modified=False)
    site.from_directory(templates_dir)
    site.from_directory(content_dir)
    site.set_values()
    site.sort()
    site.set_relationships()

    # check one level
    foo = site.root.get("foo.txt")
    assert foo == site.nodes["/foo.txt"]

    # check multiple levels
    bat = site.root.get("dir1", "dir2", "dir3", "bat.txt")
    assert bat == site.nodes["/dir1/dir2/dir3/bat.txt"]

    # check period (.), which means staying in the same place
    bat = site.root.get("dir1", "dir2", "dir3", ".", "", "bat.txt")
    assert bat == site.nodes["/dir1/dir2/dir3/bat.txt"]

    # check double period (..), which means moving up one directory
    bar = bat.get("..", "..", "..", "bar.txt")
    assert bar == site.nodes["/dir1/bar.txt"]

    # check navigation across file trees
    this = bat.get("..", "..", "..", "dir2", "this.txt")
    assert this == site.nodes["/dir1/dir2/this.txt"]
