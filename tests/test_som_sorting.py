
from spekulatio.som import SOM


def test_sorting_by_name(tmp_path):
    """Test sorting by name (asc)"""

    values = tmp_path / '_values.json'
    values.write_text('{"_sorting_method": "name"}')
    (tmp_path / 'aaa.rst').touch()
    (tmp_path / 'bbb.rst').touch()
    (tmp_path / 'ccc.rst').touch()
    (tmp_path / 'eee.rst').touch()
    dir1 = tmp_path / 'dir1/'
    dir1.mkdir()
    (dir1 / 'aaa.rst').touch()
    (dir1 / 'bbb.rst').touch()
    (dir1 / 'ccc.rst').touch()

    # expected outcome
    expected_result = [
        'aaa.rst',
        'bbb.rst',
        'ccc.rst',
        'dir1',
        'dir1/aaa.rst',
        'dir1/bbb.rst',
        'dir1/ccc.rst',
        'eee.rst'
    ]

    som = SOM(tmp_path)
    assert expected_result == som.list_names()


def test_sorting_by_name_reverse(tmp_path):
    """Test sorting by name (desc)"""

    values = tmp_path / '_values.json'
    values.write_text('{"_sorting_method": "name", "_sorting_direction": "desc"}')
    (tmp_path / 'aaa.rst').touch()
    (tmp_path / 'bbb.rst').touch()
    (tmp_path / 'ccc.rst').touch()
    (tmp_path / 'eee.rst').touch()
    dir1 = tmp_path / 'dir1/'
    dir1.mkdir()
    (dir1 / 'aaa.rst').touch()
    (dir1 / 'bbb.rst').touch()
    (dir1 / 'ccc.rst').touch()

    # expected outcome
    expected_result = [
        'eee.rst',
        'dir1',
        'dir1/ccc.rst',
        'dir1/bbb.rst',
        'dir1/aaa.rst',
        'ccc.rst',
        'bbb.rst',
        'aaa.rst'
    ]

    som = SOM(tmp_path)
    assert expected_result == som.list_names()


def test_sorting_by_field(tmp_path):
    """Test sorting by field."""

    values = tmp_path / '_values.json'
    values.write_text('{"_sorting_method": "field", "_sorting_data": "position"}')

    rst_template = "---\nposition: {}\n---\n\nTitle\n=====\n\nContent\n"
    (tmp_path / 'aaa.rst').write_text(rst_template.format('2'))
    (tmp_path / 'bbb.rst').touch()
    (tmp_path / 'ccc.rst').write_text(rst_template.format('1'))
    (tmp_path / 'eee.rst').write_text(rst_template.format('4'))

    dir1 = tmp_path / 'dir1/'
    dir1.mkdir()
    values_dir1 = dir1 / '_values.json'
    values_dir1.write_text('{"position": 3, "_sorting_method": "name"}')
    (dir1 / 'bbb.rst').touch()
    (dir1 / 'aaa.rst').touch()
    (dir1 / 'ccc.rst').touch()

    # expected outcome
    expected_result = [
        'ccc.rst',
        'aaa.rst',
        'dir1',
        'dir1/aaa.rst',
        'dir1/bbb.rst',
        'dir1/ccc.rst',
        'eee.rst'
    ]

    som = SOM(tmp_path)
    # for node in som.iter_nodes():
    #     print(node.path, node.data)
    assert expected_result == som.list_names()


def test_sorting_by_list(tmp_path):
    """Test sorting by list."""

    values = tmp_path / '_values.json'
    values.write_text("""
        {
            "_sorting_method": "list",
            "_sorting_data": [
                "ccc.rst",
                "aaa.rst",
                "dir1",
                "bbb.rst"
            ]
        }
    """)

    (tmp_path / 'aaa.rst').touch()
    (tmp_path / 'bbb.rst').touch()
    (tmp_path / 'ccc.rst').touch()
    (tmp_path / 'eee.rst').touch()

    dir1 = tmp_path / 'dir1/'
    dir1.mkdir()
    values_dir1 = dir1 / '_values.json'
    values_dir1.write_text('{"_sorting_method": "name"}')
    (dir1 / 'bbb.rst').touch()
    (dir1 / 'aaa.rst').touch()
    (dir1 / 'ccc.rst').touch()

    # expected outcome
    expected_result = [
        'ccc.rst',
        'aaa.rst',
        'dir1',
        'dir1/aaa.rst',
        'dir1/bbb.rst',
        'dir1/ccc.rst',
        'bbb.rst'
    ]

    som = SOM(tmp_path)
    assert expected_result == som.list_names()

