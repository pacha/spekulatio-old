
from spekulatio.som import SOM


def test_create_som(tmp_path):
    """Create a simple som."""

    # input file tree:
    #   foo.json
    #   dir1/
    #     bar.json
    foo = tmp_path / 'foo.json'
    foo.write_text('{"spam": "eggs"}')
    dir1 = tmp_path / 'dir1/'
    dir1.mkdir()
    bar = dir1 / 'bar.json'
    bar.write_text('{"spam": "eggs"}')

    # expected outcome
    expected_result = set([
        'foo.json',
        'dir1',
        'dir1/bar.json'
    ])

    som = SOM(tmp_path)
    node_names = set(som.list_names())
    assert expected_result == node_names


def test_create_empty_dirs(tmp_path):
    """Check that empty dirs are not included in som."""

    # input file tree:
    #   dir1/
    #     foo.json
    #   dir2/
    #   dir3/
    #     bar.odt
    #   dir4/
    #     _values.json
    dir1 = tmp_path / 'dir1/'
    dir1.mkdir()
    dir2 = tmp_path / 'dir2/'
    dir2.mkdir()
    dir3 = tmp_path / 'dir3/'
    dir3.mkdir()
    dir4 = tmp_path / 'dir4/'
    dir4.mkdir()
    foo = dir1 / 'foo.json'
    foo.write_text('{"spam": "eggs"}')
    bar = dir3 / 'bar.odt'
    bar.write_text('')
    values = dir4 / '_values.json'
    values.write_text('{"spam": "eggs"}')

    # expected outcome
    expected_result = set([
        'dir1',
        'dir1/foo.json'
    ])

    som = SOM(tmp_path)
    node_names = set(som.list_names())
    assert expected_result == node_names


def test_parent_relationship(tmp_path):
    """Check that the parent/child relationship is set."""

    # input file tree:
    #   foo.json
    #   dir1/
    #     bar.json
    foo = tmp_path / 'foo.json'
    foo.write_text('{"spam": "eggs"}')
    dir1 = tmp_path / 'dir1/'
    dir1.mkdir()
    bar = dir1 / 'bar.json'
    bar.write_text('{"spam": "eggs"}')

    som = SOM(tmp_path)
    assert som.root_node.parent is None

    for node in som.root_node.iter_nodes():
        siblings = node.parent.children
        assert node in siblings


def test_node_map(tmp_path):
    """Check that the parent/child relationship is set."""

    # input file tree:
    #   foo.json
    #   dir1/
    #     bar.json
    foo = tmp_path / 'foo.json'
    foo.write_text('{"spam": "eggs"}')
    dir1 = tmp_path / 'dir1/'
    dir1.mkdir()
    bar = dir1 / 'bar.json'
    bar.write_text('{"spam": "eggs"}')

    som = SOM(tmp_path)

    for node in som.iter_nodes():
        assert som.map[str(node)] == node

