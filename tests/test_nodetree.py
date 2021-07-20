from pathlib import Path

import pytest

from spekulatio.models import Site
from spekulatio.models.input_dirs import InputDir
from spekulatio.paths import default_input_dir_path
from spekulatio.exceptions import SpekulatioReadError


def test_empty_dir_site(fixtures_path):

    # source files path
    content_path = fixtures_path / "nodetree" / "empty-dir" / "content"
    content_dir = InputDir(content_path, "site_content")

    site = Site(output_path=None, only_modified=False)
    site.from_directory(content_dir)

    # check root
    assert site.root is not None
    assert site.root.depth == 0
    assert site.root.is_dir is True
    assert len(site.root.children) == 0


def test_one_node_site(fixtures_path):

    # source files path
    content_path = fixtures_path / "nodetree" / "one-node" / "content"
    content_dir = InputDir(content_path, "site_content")

    site = Site(output_path=None, only_modified=False)
    site.from_directory(content_dir)

    # check root
    assert site.root is not None
    assert site.root.depth == 0
    assert site.root.is_dir is True
    assert len(site.root.children) == 1

    # check foo node
    foo = site.root.children[0]
    assert foo.depth == 1
    assert foo.root == site.root
    assert foo.parent == site.root
    assert foo.relative_src_path.name == "foo.md"
    assert foo.action.extension_change == ".html"

    # check foo's parent
    index = site.nodes["/index.html"]
    assert index.depth == 1
    assert index.root == site.root
    assert index.parent is None
    assert index.relative_src_path.name == "index.md"
    assert index.action.extension_change == ".html"


def test_multi_node_site(fixtures_path):

    # source files path
    content_path = fixtures_path / "nodetree" / "multi-node" / "content"
    content_dir = InputDir(content_path, "site_content")

    site = Site(output_path=None, only_modified=False)
    site.from_directory(content_dir)

    # check root
    assert site.root is not None
    assert len(site.root.children) == 2

    # check first level
    level1_names = set([node.name for node in site.root.children])
    assert level1_names == {"dir1", "dir2"}

    # check dir1
    dir1 = site.nodes["/dir1"]
    dir1_names = set([node.name for node in dir1.children])
    assert dir1_names == {"dir1-a", "index1.html"}

    # check dir2
    dir2 = site.nodes["/dir2"]
    dir2_names = set([node.name for node in dir2.children])
    assert dir2_names == {"index2.html"}


def test_multi_content_site(fixtures_path):

    # source files path
    content1_path = fixtures_path / "nodetree" / "multi-content" / "content1"
    content1_dir = InputDir(content1_path, "site_content")
    content2_path = fixtures_path / "nodetree" / "multi-content" / "content2"
    content2_dir = InputDir(content2_path, "site_content")

    site = Site(output_path=None, only_modified=False)
    site.from_directory(content1_dir)
    site.from_directory(content2_dir)

    # check first level
    level1_names = set([node.name for node in site.root.children])
    assert level1_names == {"dir1", "foo.html", "bar.html"}

    # check dir1
    dir1 = site.nodes["/dir1"]
    dir1_names = set([node.name for node in dir1.children])
    assert dir1_names == {"baz.html"}


def test_multi_template_site(fixtures_path):

    # source files path
    template1_path = fixtures_path / "nodetree" / "multi-template" / "template1"
    template1_dir = InputDir(template1_path, "site_templates")
    template2_path = fixtures_path / "nodetree" / "multi-template" / "template2"
    template2_dir = InputDir(template2_path, "site_templates")
    content1_path = fixtures_path / "nodetree" / "multi-template" / "content1"
    content1_dir = InputDir(content1_path, "site_content")
    content2_path = fixtures_path / "nodetree" / "multi-template" / "content2"
    content2_dir = InputDir(content2_path, "site_content")

    site = Site(output_path=None, only_modified=False)
    site.from_directory(template1_dir)
    site.from_directory(template2_dir)
    site.from_directory(content1_dir)
    site.from_directory(content2_dir)

    # check first level
    level1_names = set([node.name for node in site.root.children])
    assert level1_names == {"dir1", "dir2", "dir3"}

    # check dir1
    dir1 = site.nodes["/dir1"]
    dir1_names = set([node.name for node in dir1.children])
    assert dir1_names == {"one-pixel.png", "another-one-pixel.png"}

    # check dir2
    dir2 = site.nodes["/dir2"]
    dir2_names = set([node.name for node in dir2.children])
    assert dir2_names == {"foo.html", "image.png"}

    # check that 'foo.md' in 'content2' overrides 'foo.md' in 'content1'
    foo_html = site.nodes["/dir2/foo.html"]
    assert str(foo_html.src_path) == str(content2_path / "dir2/foo.md")

    # check dir3
    dir3 = site.nodes["/dir3"]
    dir3_names = set([node.name for node in dir3.children])
    assert dir3_names == {"style.css"}


def test_ambiguous_content(fixtures_path):

    # source files path
    content_path = fixtures_path / "nodetree" / "ambiguous-content" / "content"
    content_dir = InputDir(content_path, "site_content")

    site = Site(output_path=None, only_modified=False)
    with pytest.raises(SpekulatioReadError):
        site.from_directory(content_dir)
