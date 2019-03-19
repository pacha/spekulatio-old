import time

from spekulatio.build_file_tree import build_file_tree


def test_basic_file_tree(tmp_path):
    """Create a basic file tree."""

    # source
    src_path = tmp_path / 'src/'
    src_path.mkdir()
    foo = src_path / 'foo.txt'
    foo.write_text('foo content')
    baz = src_path / 'baz.css'
    baz.write_text('body { background: red; }')
    dir1 = src_path / 'dir1/'
    dir1.mkdir()
    bar = dir1 / 'bar.json'
    bar.write_text('{"spam": "eggs"}')

    # destination
    dst_path = tmp_path / 'dst/'
    dst_path.mkdir()

    # build tree
    build_file_tree(src_path, dst_path, no_cache=True, actions={})

    dst_foo = dst_path / 'foo.txt'
    dst_baz = dst_path / 'baz.css'
    dst_bar = dst_path / 'dir1/bar.json'
    dst_dir1 = dst_path / 'dir1/'

    assert dst_foo.is_file()
    assert dst_baz.is_file()
    assert dst_bar.is_file()
    assert dst_dir1.is_dir()

    assert dst_foo.read_text() == 'foo content'


def test_ignore_sources(tmp_path):
    """Make build_file_tree to ignore certain files."""

    # source
    src_path = tmp_path / 'src/'
    src_path.mkdir()
    foo = src_path / 'foo.txt'
    foo.write_text('foo content')
    baz = src_path / 'baz.css'
    baz.write_text('body { background: red; }')
    dir1 = src_path / 'dir1/'
    dir1.mkdir()
    bar = dir1 / 'bar.json'
    bar.write_text('{"spam": "eggs"}')

    # destination
    dst_path = tmp_path / 'dst/'
    dst_path.mkdir()

    # build tree
    def ignore(*args, **kwargs):
        pass
    build_file_tree(src_path, dst_path, no_cache=True, actions={'.css': ignore})

    dst_foo = dst_path / 'foo.txt'
    dst_baz = dst_path / 'baz.css'
    dst_bar = dst_path / 'dir1/bar.json'

    assert dst_foo.is_file()
    assert not dst_baz.is_file()
    assert dst_bar.is_file()

    assert dst_foo.read_text() == 'foo content'


def test_transform_sources(tmp_path):
    """Make build_file_tree to transform certain files."""

    # source
    src_path = tmp_path / 'src/'
    src_path.mkdir()
    foo = src_path / 'foo.txt'
    foo.write_text('foo content')
    baz = src_path / 'baz.css'
    baz.write_text('body { background: red; }')

    # destination
    dst_path = tmp_path / 'dst/'
    dst_path.mkdir()

    # build tree
    def make_uppercase(root_src_path, src_path, root_dst_path, dst_path):
        src_content = src_path.read_text()
        dst_content = src_content.upper()
        dst_path.write_text(dst_content)

    build_file_tree(
        src_path, dst_path, no_cache=True,
        actions={'.txt': make_uppercase}
    )

    dst_foo = dst_path / 'foo.txt'
    dst_baz = dst_path / 'baz.css'

    assert dst_foo.is_file()
    assert dst_baz.is_file()

    assert dst_foo.read_text() == 'FOO CONTENT'
    assert dst_baz.read_text() == 'body { background: red; }'


def test_transform_suffixes(tmp_path):
    """Check that suffixes are transformed when specified."""

    # source
    src_path = tmp_path / 'src/'
    src_path.mkdir()
    foo = src_path / 'foo.rst'
    foo.write_text('foo content')

    # destination
    dst_path = tmp_path / 'dst/'
    dst_path.mkdir()

    # build tree
    def just_copy(root_src_path, src_path, root_dst_path, dst_path):
        dst_path.write_text(src_path.read_text())

    build_file_tree(
        src_path, dst_path, no_cache=True,
        actions={'.rst': ('.html', just_copy)}
    )

    wrong_dst_foo = dst_path / 'foo.rst'
    dst_foo = dst_path / 'foo.html'

    assert not wrong_dst_foo.is_file()
    assert dst_foo.is_file()
    assert dst_foo.read_text() == 'foo content'


def test_basic_file_tree_cache(tmp_path):
    """Check that targets aren't overwritten when src file is unchanged."""

    # source
    src_path = tmp_path / 'src/'
    src_path.mkdir()
    foo = src_path / 'foo.txt'
    foo.write_text('foo content')

    # destination
    dst_path = tmp_path / 'dst/'
    dst_path.mkdir()

    # build tree
    time.sleep(0.1)
    build_file_tree(src_path, dst_path, no_cache=False, actions={})

    dst_foo = dst_path / 'foo.txt'

    # check that dst timestamp is older than that of the original file
    assert dst_foo.stat().st_mtime >= foo.stat().st_mtime

    # check that dst doesn't get overwritten if src is unchanged
    prev_timestamp = dst_foo.stat().st_mtime
    time.sleep(0.1)
    build_file_tree(src_path, dst_path, no_cache=False, actions={})
    assert dst_foo.stat().st_mtime == prev_timestamp

    # modify original file to check that destination changes
    time.sleep(0.1)
    foo.touch()
    build_file_tree(src_path, dst_path, no_cache=False, actions={})
    assert dst_foo.stat().st_mtime >= prev_timestamp

