
from pathlib import Path

import pytest

from spekulatio.models import Site
from spekulatio.models.filetrees import content_conf
from spekulatio.models.filetrees import template_conf
from spekulatio.exceptions import SpekulatioReadError

def test_root(fixtures_path):

    # source files path
    content_path = fixtures_path / 'relationships' / 'root' / 'content'

    site = Site(build_path=None, only_modified=False)
    site.from_directory(content_path, content_conf)

    # check all nodes
    dir1 = site.nodes['/dir1']
    assert dir1.root == site.root

    foo = site.nodes['/foo.html']
    assert foo.root == site.root

    dir2 = site.nodes['/dir1/dir2']
    assert dir2.root == site.root

    bar = site.nodes['/dir1/bar.html']
    assert bar.root == site.root

    baz = site.nodes['/dir1/dir2/baz.js']
    assert baz.root == site.root

def test_prev_next(fixtures_path):

    # source files path
    content_path = fixtures_path / 'relationships' / 'prev-next' / 'content'

    site = Site(build_path=None, only_modified=False)
    site.from_directory(content_path, content_conf)
    site.sort()
    site.set_relationships()

    # check all nodes
    foo = site.nodes['/foo.html']
    dir1 = site.nodes['/dir1']

    dir2 = site.nodes['/dir1/dir2']

    bak = site.nodes['/dir1/dir2/bak.html']
    bat = site.nodes['/dir1/dir2/bat.html']

    baz = site.nodes['/dir1/baz.html']

    bar = site.nodes['/bar.html']

    assert site.root.next == foo
    assert foo.next == dir1
    assert dir1.next == dir2
    assert dir2.next == bak
    assert bak.next == bat
    assert bat.next == baz
    assert baz.next == bar


def test_siblings(fixtures_path):

    # source files path
    content_path = fixtures_path / 'relationships' / 'siblings' / 'content'

    site = Site(build_path=None, only_modified=False)
    site.from_directory(content_path, content_conf)
    site.sort()
    site.set_relationships()

    # check all nodes
    foo = site.nodes['/foo.html']
    dir1 = site.nodes['/dir1']
    bar = site.nodes['/bar.html']

    dir2 = site.nodes['/dir1/dir2']
    baz = site.nodes['/dir1/baz.html']

    bak = site.nodes['/dir1/dir2/bak.html']
    bat = site.nodes['/dir1/dir2/bat.html']

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

