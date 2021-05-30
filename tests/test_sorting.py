
from pathlib import Path

import pytest

from spekulatio.models import Site
from spekulatio.models.filetrees import content_conf
from spekulatio.models.filetrees import template_conf
from spekulatio.exceptions import SpekulatioReadError

def test_default_sorting(fixtures_path):

    # source files path
    content_path = fixtures_path / 'sorting' / 'default-sorting' / 'content'

    site = Site(build_path=None, only_modified=False)
    site.from_directory(content_path, content_conf)
    site.set_values()
    site.sort()

    # check dir1
    dir1 = site.nodes['/dir1']
    child_names = [node.name for node in dir1.children]
    assert child_names == ['a.html', 'b.html', 'c.html']

    # check dir2
    dir2 = site.nodes['/dir2']
    child_names = [node.name for node in dir2.children]
    assert child_names == ['bar.html', 'baz.css', 'foo.html']

    # check dir3
    dir3 = site.nodes['/dir3']
    child_names = [node.name for node in dir3.children]
    assert child_names == ['dir4', 'foo.html']


def test_manual_sorting(fixtures_path):

    # source files path
    content_path = fixtures_path / 'sorting' / 'manual-sorting' / 'content'

    site = Site(build_path=None, only_modified=False)
    site.from_directory(content_path, content_conf)
    site.set_values()
    site.sort()

    # check dir1
    dir1 = site.nodes['/dir1']
    child_names = [node.name for node in dir1.children]
    assert child_names == ['b.html', 'c.html', 'a.html']

    # check dir2
    dir2 = site.nodes['/dir2']
    child_names = [node.name for node in dir2.children]
    assert child_names == ['foo.html', 'baz.css', 'bar.html']

    # check dir3
    dir3 = site.nodes['/dir3']
    child_names = [node.name for node in dir3.children]
    assert child_names == ['foo.html', 'dir4']


def test_mixed_sorting(fixtures_path):

    # source files path
    content_path = fixtures_path / 'sorting' / 'mixed-sorting' / 'content'

    site = Site(build_path=None, only_modified=False)
    site.from_directory(content_path, content_conf)
    site.set_values()
    site.sort()

    # check dir1
    dir1 = site.nodes['/dir1']
    child_names = [node.name for node in dir1.children]
    assert child_names == ['e.html', 'b.html', 'a.html', 'c.html', 'd.html', 'f.html']

    # check dir2
    dir2 = site.nodes['/dir2']
    child_names = [node.name for node in dir2.children]
    assert child_names == ['e.html', 'b.html', 'a.html', 'c.html', 'd.html', 'f.html']

    # check dir3
    dir3 = site.nodes['/dir3']
    child_names = [node.name for node in dir3.children]
    assert child_names == ['a.html', 'c.html', 'd.html', 'f.html', 'e.html', 'b.html']

    # check dir4
    dir4 = site.nodes['/dir4']
    child_names = [node.name for node in dir4.children]
    assert child_names == ['e.html', 'a.html', 'c.html', 'd.html', 'f.html', 'b.html']

