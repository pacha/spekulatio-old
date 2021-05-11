
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

    with pytest.raises(SpekulatioReadError):
        site.from_directory(content_path, content_conf)


def test_values_file(fixtures_path):

    # source files path
    content_path = fixtures_path / 'values' / 'values-file' / 'content'

    site = Site(build_path=None, only_modified=False)
    site.from_directory(content_path, content_conf)

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

    # source files path
    content_path = fixtures_path / 'values' / 'value-scopes' / 'content'

    site = Site(build_path=None, only_modified=False)
    site.from_directory(content_path, content_conf)

    # check root
    assert 'local_var' not in site.root.branch_data
    assert 'local_var' not in site.root.level_data
    assert 'local_var' in site.root.local_data

    assert 'level_var' not in site.root.branch_data
    assert 'level_var' in site.root.level_data
    assert 'level_var' in site.root.local_data

    assert 'branch_var' in site.root.branch_data
    assert 'branch_var' in site.root.level_data
    assert 'branch_var' in site.root.local_data

    assert 'default_syntax_var' in site.root.branch_data
    assert 'default_syntax_var' in site.root.level_data
    assert 'default_syntax_var' in site.root.local_data

    # check dir1
    dir1 = site.nodes['/dir1']

    assert 'local_var' not in dir1.branch_data
    assert 'local_var' not in dir1.level_data
    assert 'local_var' not in dir1.local_data

    assert 'level_var' not in dir1.branch_data
    assert 'level_var' not in dir1.level_data
    assert 'level_var' in dir1.local_data

    assert 'branch_var' in dir1.branch_data
    assert 'branch_var' in dir1.level_data
    assert 'branch_var' in dir1.local_data

    assert 'default_syntax_var' in dir1.branch_data
    assert 'default_syntax_var' in dir1.level_data
    assert 'default_syntax_var' in dir1.local_data

    # check foo.md
    foo = site.nodes['/dir1/foo.html']

    assert 'local_var' not in foo.branch_data
    assert 'local_var' not in foo.level_data
    assert 'local_var' not in foo.local_data

    assert 'level_var' not in foo.branch_data
    assert 'level_var' not in foo.level_data
    assert 'level_var' not in foo.local_data

    assert 'branch_var' in foo.branch_data
    assert 'branch_var' in foo.level_data
    assert 'branch_var' in foo.local_data

    assert 'default_syntax_var' in foo.branch_data
    assert 'default_syntax_var' in foo.level_data
    assert 'default_syntax_var' in foo.local_data

