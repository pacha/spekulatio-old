
from pathlib import Path

import pytest

from spekulatio.models import Site
from spekulatio.models.filetrees import content_conf
from spekulatio.models.filetrees import template_conf
from spekulatio.exceptions import SpekulatioReadError

def test_frontmatter_values(fixtures_path):

    # source files path
    content_path = fixtures_path / 'values' / 'frontmatter' / 'content'

    site = Site(build_path=None, only_modified=False)
    site.from_directory(content_path, content_conf)
    site.set_values()

    # check node values
    node = site.nodes['/foo.html']
    expected_data = {
        'a': 1,
        'b': 'this',
        'c': {
            'c1': 'one',
            'c2': 'two',
        },
        'd': ['one', 'two'],
    }
    assert node.user_data == expected_data


def test_frontmatter_error(fixtures_path):

    # source files path
    content_path = fixtures_path / 'values' / 'frontmatter-error' / 'content'

    site = Site(build_path=None, only_modified=False)
    site.from_directory(content_path, content_conf)

    with pytest.raises(SpekulatioReadError):
        site.set_values()


def test_values_file(fixtures_path):

    # source files path
    content_path = fixtures_path / 'values' / 'values-file' / 'content'

    site = Site(build_path=None, only_modified=False)
    site.from_directory(content_path, content_conf)
    site.set_values()

    # check node values
    expected_data = {
        'a': 1,
        'b': 'this',
        'c': {
            'c1': 'one',
            'c2': 'two',
        },
        'd': ['one', 'two'],
    }
    assert site.root.user_data == expected_data


def test_value_scopes(fixtures_path):
    """Check how values in different scopes defined at root are passed down the tree."""

    # source files path
    content_path = fixtures_path / 'values' / 'value-scopes' / 'content'

    site = Site(build_path=None, only_modified=False)
    site.from_directory(content_path, content_conf)
    site.set_values()

    # check root
    assert 'local_var' not in site.root.branch_data
    assert 'local_var' not in site.root.level_data
    assert 'local_var' in site.root.data

    assert 'level_var' not in site.root.branch_data
    assert 'level_var' in site.root.level_data
    assert 'level_var' in site.root.data

    assert 'branch_var' in site.root.branch_data
    assert 'branch_var' not in site.root.level_data
    assert 'branch_var' in site.root.data

    assert 'default_syntax_var' in site.root.branch_data
    assert 'default_syntax_var' not in site.root.level_data
    assert 'default_syntax_var' in site.root.data

    # check dir1
    dir1 = site.nodes['/dir1']

    assert 'local_var' not in dir1.branch_data
    assert 'local_var' not in dir1.level_data
    assert 'local_var' not in dir1.data

    assert 'level_var' not in dir1.branch_data
    assert 'level_var' not in dir1.level_data
    assert 'level_var' in dir1.data

    assert 'branch_var' in dir1.branch_data
    assert 'branch_var' not in dir1.level_data
    assert 'branch_var' in dir1.data

    assert 'default_syntax_var' in dir1.branch_data
    assert 'default_syntax_var' not in dir1.level_data
    assert 'default_syntax_var' in dir1.data

    # check foo.md
    foo = site.nodes['/dir1/foo.html']

    assert 'local_var' not in foo.branch_data
    assert 'local_var' not in foo.level_data
    assert 'local_var' not in foo.data

    assert 'level_var' not in foo.branch_data
    assert 'level_var' not in foo.level_data
    assert 'level_var' not in foo.data

    assert 'branch_var' in foo.branch_data
    assert 'branch_var' not in foo.level_data
    assert 'branch_var' in foo.data

    assert 'default_syntax_var' in foo.branch_data
    assert 'default_syntax_var' not in foo.level_data
    assert 'default_syntax_var' in foo.data

def test_overwriting(fixtures_path):

    # source files path
    content_path = fixtures_path / 'values' / 'overwriting' / 'content'

    site = Site(build_path=None, only_modified=False)
    site.from_directory(content_path, content_conf)
    site.set_values()

    # check foo
    foo = site.nodes['/dir1/foo.html']
    assert foo.user_data == {'foo_var': 1, 'level_var': 2, 'branch_var': 3}

    # check bar
    bar = site.nodes['/dir1/bar.html']
    assert bar.user_data == {'bar_var': 2, 'level_var': 'overwritten', 'branch_var': 3}

    # check baz
    baz = site.nodes['/dir1/baz.html']
    assert baz.user_data == {'baz_var': 3, 'level_var': 2, 'branch_var': 'overwritten'}


def test_overwriting_filetrees(fixtures_path):

    # source files path
    content_path1 = fixtures_path / 'values' / 'overwriting-filetrees' / 'content1'
    content_path2 = fixtures_path / 'values' / 'overwriting-filetrees' / 'content2'

    site = Site(build_path=None, only_modified=False)
    site.from_directory(content_path1, content_conf)
    site.from_directory(content_path2, content_conf)
    site.set_values()

    # check foo
    foo = site.nodes['/dir1/foo.html']
    assert foo.user_data == {'default_var': 0, 'foo_var': 1, 'level_var': 2, 'branch_var': 3}

    # check bar
    bar = site.nodes['/dir1/bar.html']
    assert bar.user_data == {'default_var': 'this', 'bar_var': 2, 'level_var': 'overwritten', 'branch_var': 3}

    # check baz
    baz = site.nodes['/dir1/baz.html']
    assert baz.user_data == {'default_var': 'that', 'baz_var': 3, 'level_var': 2, 'branch_var': 'overwritten'}


def test_default_values(fixtures_path):

    # source files path
    content_path1 = fixtures_path / 'values' / 'default-values' / 'content1'
    content_path2 = fixtures_path / 'values' / 'default-values' / 'content2'

    site = Site(build_path=None, only_modified=False)
    site.from_directory(content_path1, content_conf)
    site.from_directory(content_path2, content_conf)
    site.set_values()

    # check dir1
    dir1 = site.nodes['/dir1']
    assert dir1.user_data == {'default_var1': 1, 'default_var2': 'b', 'default_var3': 'c'}

    # check foo
    foo = site.nodes['/dir1/foo.html']
    assert foo.user_data == {'default_var1': 1, 'default_var2': 'b', 'default_var3': 3}


def test_default_inheritance(fixtures_path):

    # source files path
    content_path = fixtures_path / 'values' / 'default-inheritance' / 'content'
    template_path = fixtures_path / 'values' / 'default-inheritance' / 'templates'

    site = Site(build_path=None, only_modified=False)
    site.from_directory(template_path, template_conf)
    site.from_directory(content_path, content_conf)
    site.set_values()

    # check default template from root
    root = site.nodes['/']
    assert root.data['_template'] == 'two-cols.html'

    # check foo
    foo = site.nodes['/foo.html']
    assert foo.data['_template'] == 'two-cols.html'

    # check bar
    bar = site.nodes['/bar.html']
    assert bar.data['_template'] == 'three-cols.html'

    # check baz
    baz = site.nodes['/baz.html']
    assert baz.data['_template'] == 'one-col.html'


def test_operations(fixtures_path):

    # source files path
    content_path = fixtures_path / 'values' / 'operations' / 'content'

    site = Site(build_path=None, only_modified=False)
    site.from_directory(content_path, content_conf)
    site.set_values()

    # check delete operation
    delete = site.nodes['/delete.html']
    assert 'my_list' not in delete.user_data

    # check append operation
    append = site.nodes['/append.html']
    assert append.user_data['my_list'] == ['a', 'b', 'c', 'd']

    # check merge operation
    merge = site.nodes['/merge.html']
    assert merge.user_data['my_dict'] == {'a': 1, 'b': 4, 'c': 3, 'd': 5}

    # check replace operation
    replace = site.nodes['/replace.html']
    assert replace.user_data['my_scalar'] == 7
    assert replace.user_data['my_list'] == ['b', 'e']
    assert replace.user_data['my_dict'] == {'b': 2, 'e': 6}

def test_operations_wrong_append(fixtures_path):

    # source files path
    content_path = fixtures_path / 'values' / 'operations-wrong-append' / 'content'

    site = Site(build_path=None, only_modified=False)
    site.from_directory(content_path, content_conf)
    with pytest.raises(SpekulatioReadError):
        site.set_values()

def test_operations_wrong_merge(fixtures_path):

    # source files path
    content_path = fixtures_path / 'values' / 'operations-wrong-merge' / 'content'

    site = Site(build_path=None, only_modified=False)
    site.from_directory(content_path, content_conf)
    with pytest.raises(SpekulatioReadError):
        site.set_values()

def test_operations_wrong_delete(fixtures_path):

    # source files path
    content_path = fixtures_path / 'values' / 'operations-wrong-delete' / 'content'

    site = Site(build_path=None, only_modified=False)
    site.from_directory(content_path, content_conf)
    with pytest.raises(SpekulatioReadError):
        site.set_values()

def test_duplicate_values(fixtures_path):

    # source files path
    content_path = fixtures_path / 'values' / 'duplicate-values' / 'content'

    site = Site(build_path=None, only_modified=False)
    site.from_directory(content_path, content_conf)
    site.set_values()

    # check directory node
    dir_node = site.nodes['/dir1']
    expected_data = {'foo': 3, 'bar': 2, 'baz': 2}
    assert dir_node.user_data == expected_data

    # check file node
    file_node = site.nodes['/file.html']
    expected_data = {'foo': 3, 'bar': 2, 'baz': 2}
    assert file_node.user_data == expected_data

