
from spekulatio.som import SOM


def test_data_inheritance_in_same_dir(tmp_path):
    """Check that node dir values are inherit by its inmediate children"""

    values = tmp_path / '_values.json'
    values.write_text('{"a": "root", "b": "root"}')
    foo = tmp_path / 'foo.json'
    foo.write_text('{"b": "foo"}')

    som = SOM(tmp_path)
    assert len(som.root_node.children) == 1
    node_foo = som.map['foo.json']
    assert dict(node_foo.data) == {"a": "root", "b": "foo"}


def test_data_inheritance_in_different_levels(tmp_path):
    """Check that node dir values are inherit by its descentants"""

    values = tmp_path / '_values.json'
    values.write_text('{"a": "root", "b": "root", "c": "root", "d": "root"}')
    dir1 = tmp_path / 'dir1/'
    dir1.mkdir()
    foo = dir1 / 'foo.json'
    foo.write_text('{"a": "foo"}')
    dir2 = dir1 / 'dir2/'
    dir2.mkdir()
    bar = dir2 / '_values.json'
    bar.write_text('{"b": "dir2"}')
    bar = dir2 / 'bar.json'
    bar.write_text('{"c": "bar"}')

    som = SOM(tmp_path)
    assert len(som.list_names()) == 4
    assert dict(som.root_node.data) == {"a": "root", "b": "root", "c": "root", "d": "root"}
    node_dir1 = som.map['dir1']
    assert dict(node_dir1.data) == {"a": "root", "b": "root", "c": "root", "d": "root"}
    node_foo = som.map['dir1/foo.json']
    assert dict(node_foo.data) == {"a": "foo", "b": "root", "c": "root", "d": "root"}
    node_dir2 = som.map['dir1/dir2']
    assert dict(node_dir2.data) == {"a": "root", "b": "dir2", "c": "root", "d": "root"}
    node_bar = som.map['dir1/dir2/bar.json']
    assert dict(node_bar.data) == {"a": "root", "b": "dir2", "c": "bar", "d": "root"}

