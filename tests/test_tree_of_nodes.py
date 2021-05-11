
from pathlib import Path

from spekulatio.models import Site
from spekulatio.models.filetrees import content_conf
from spekulatio.models.filetrees import template_conf


def test_empty_dir_site(fixtures_path):

    # source files path
    content_path = fixtures_path / 'tree-of-nodes' / 'empty-dir' / 'content'

    site = Site(build_path=None, only_modified=False)
    site.from_directory(content_path, content_conf)

    # check root
    assert site.root is not None
    assert site.root.depth == 0
    assert site.root.is_dir is True
    assert len(site.root.children) == 0

def test_one_node_site(fixtures_path):

    # source files path
    content_path = fixtures_path / 'tree-of-nodes' / 'one-node' / 'content'

    site = Site(build_path=None, only_modified=False)
    site.from_directory(content_path, content_conf)

    # check root
    assert site.root is not None
    assert site.root.depth == 0
    assert site.root.is_dir is True
    assert len(site.root.children) == 1

    # check only node
    only_node = site.root.children[0]
    assert only_node.depth == 1
    assert only_node.root == site.root
    assert only_node.parent == site.root
    assert only_node.relative_src_path.name == 'index.md'
    assert only_node.action.extension_change == '.html'

def test_multi_node_site(fixtures_path):

    # source files path
    content_path = fixtures_path / 'tree-of-nodes' / 'multi-node' / 'content'

    site = Site(build_path=None, only_modified=False)
    site.from_directory(content_path, content_conf)

    # check root
    assert site.root is not None
    assert len(site.root.children) == 3

    # check first level
    level1_names = set([node.name for node in site.root.children])
    assert level1_names == {'dir1', 'dir2', 'index.html'}

    # check dir1
    dir1 = site.nodes['/dir1']
    dir1_names = set([node.name for node in dir1.children])
    assert dir1_names == {'dir1-a', 'index1.html'}

    # check dir2
    dir2 = site.nodes['/dir2']
    dir2_names = set([node.name for node in dir2.children])
    assert dir2_names == {'index2.html'}

def test_multi_content_site(fixtures_path):

    # source files path
    content1_path = fixtures_path / 'tree-of-nodes' / 'multi-content' / 'content1'
    content2_path = fixtures_path / 'tree-of-nodes' / 'multi-content' / 'content2'

    site = Site(build_path=None, only_modified=False)
    site.from_directory(content1_path, content_conf)
    site.from_directory(content2_path, content_conf)

    # check first level
    level1_names = set([node.name for node in site.root.children])
    assert level1_names == {'dir1', 'foo.html', 'bar.html'}

    # check dir1
    dir1 = site.nodes['/dir1']
    dir1_names = set([node.name for node in dir1.children])
    assert dir1_names == {'baz.html'}

def test_multi_template_site(fixtures_path):

    # source files path
    template1_path = fixtures_path / 'tree-of-nodes' / 'multi-template' / 'template1'
    template2_path = fixtures_path / 'tree-of-nodes' / 'multi-template' / 'template2'
    content1_path = fixtures_path / 'tree-of-nodes' / 'multi-template' / 'content1'
    content2_path = fixtures_path / 'tree-of-nodes' / 'multi-template' / 'content2'

    site = Site(build_path=None, only_modified=False)
    site.from_directory(template1_path, template_conf)
    site.from_directory(template2_path, template_conf)
    site.from_directory(content1_path, content_conf)
    site.from_directory(content2_path, content_conf)

    # check first level
    level1_names = set([node.name for node in site.root.children])
    assert level1_names == {'dir1', 'dir2', 'dir3', 'index.html'}

    # check dir1
    dir1 = site.nodes['/dir1']
    dir1_names = set([node.name for node in dir1.children])
    assert dir1_names == {'one-pixel.png', 'another-one-pixel.png'}

    # check dir2
    dir2 = site.nodes['/dir2']
    dir2_names = set([node.name for node in dir2.children])
    assert dir2_names == {'foo.html', 'image.png'}

    # check that 'foo.md' in 'content2' overrides 'foo.md' in 'content1'
    foo_html = site.nodes['/dir2/foo.html']
    assert str(foo_html.src_path) == str(content2_path / 'dir2/foo.md')

    # check dir3
    dir3 = site.nodes['/dir3']
    dir3_names = set([node.name for node in dir3.children])
    assert dir3_names == {'style.css'}

