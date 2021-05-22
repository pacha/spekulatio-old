
from pathlib import Path

from spekulatio.models.filetrees import get_filetype


def test_get_known_filetype():
    """Recognize known filetype."""

    path = Path('this/is/a/markdown/file.mdwn')
    filetype = get_filetype(path)
    assert filetype == "md"

def test_get_unknown_filetype():
    """Return filetype for unknown file."""

    path = Path('this/is/a/unknown/file.foobar')
    filetype = get_filetype(path)
    assert filetype == "<file>"

def test_get_directory_filetype(fixtures_path):
    """Return filetype of actual directory"""

    path = fixtures_path / 'filetypes' /'empty-dir'
    filetype = get_filetype(path)
    assert filetype == "<dir>"

