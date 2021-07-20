from pathlib import Path

import pytest

from spekulatio.exceptions import SpekulatioValueError
from spekulatio.models.filetypes import FiletypeMap


def test_filetype_map_extension_entry():
    filetype_map = FiletypeMap()
    filetype_map.update(
        [
            {
                "name": "jpeg",
                "extensions": [".jpeg", ".jpg"],
            }
        ]
    )

    # the new filetype exists
    assert "jpeg" in filetype_map.get_filetype_names()

    # the regex is correct
    filetype = filetype_map.map["jpeg"]
    assert filetype.pattern.pattern == r"^.*(\.jpeg|\.jpg)"

    # the filetype is recognized given a file path
    assert filetype_map.get_filetype_name(Path("foo.jpeg")) == "jpeg"
    assert filetype_map.get_filetype_name(Path("foo.jpg")) == "jpeg"
    assert filetype_map.get_filetype_name(Path("foo.png")) is None


def test_filetype_map_extension_entry_without_starting_period():
    filetype_map = FiletypeMap()
    filetype_map.update(
        [
            {
                "name": "jpeg",
                "extensions": ["jpeg", "jpg"],
            }
        ]
    )

    # the filetype is recognized given a file path
    assert filetype_map.get_filetype_name(Path("foo.jpeg")) == "jpeg"
    assert filetype_map.get_filetype_name(Path("foo.jpg")) == "jpeg"
    assert filetype_map.get_filetype_name(Path("foo.png")) is None


def test_filetype_map_extension_entry_with_wrong_scope():
    filetype_map = FiletypeMap()
    with pytest.raises(SpekulatioValueError):
        filetype_map.update(
            [
                {
                    "name": "jpeg",
                    "extensions": ["jpeg", "jpg"],
                    "scope": "full-path",
                }
            ]
        )


def test_filetype_map_filetype_regex_entry():
    filetype_map = FiletypeMap()
    filetype_map.update(
        [
            {
                "name": "has-foo",
                "regex": "^.*foo.*$",
                "scope": "filename",
            }
        ]
    )

    # the filetype is recognized given a file path
    assert filetype_map.get_filetype_name(Path("foo.jpeg")) == "has-foo"
    assert filetype_map.get_filetype_name(Path("this-foo.jpg")) == "has-foo"
    assert filetype_map.get_filetype_name(Path("bar.png")) is None
    assert filetype_map.get_filetype_name(Path("/foo/bar.png")) is None


def test_filetype_map_full_path_regex_entry():
    filetype_map = FiletypeMap()
    filetype_map.update(
        [
            {
                "name": "has-foo",
                "regex": "^.*foo.*$",
                "scope": "full-path",
            }
        ]
    )

    # the filetype is recognized given a file path
    assert filetype_map.get_filetype_name(Path("foo.jpeg")) == "has-foo"
    assert filetype_map.get_filetype_name(Path("this-foo.jpg")) == "has-foo"
    assert filetype_map.get_filetype_name(Path("bar.png")) is None
    assert filetype_map.get_filetype_name(Path("/foo/bar.png")) is "has-foo"


def test_filetype_map_default_regex_scope_entry():
    filetype_map = FiletypeMap()
    filetype_map.update(
        [
            {
                "name": "has-foo",
                "regex": "^.*foo.*$",
            }
        ]
    )

    # the filetype is recognized given a file path
    assert filetype_map.get_filetype_name(Path("foo.jpeg")) == "has-foo"
    assert filetype_map.get_filetype_name(Path("this-foo.jpg")) == "has-foo"
    assert filetype_map.get_filetype_name(Path("bar.png")) is None
    assert filetype_map.get_filetype_name(Path("/foo/bar.png")) is None


def test_filetype_map_priority():
    # check one order
    filetype_map = FiletypeMap()
    filetype_map.update(
        [
            {
                "name": "has-foobar",
                "regex": r"^.*foobar.*$",
            },
            {
                "name": "has-foo",
                "regex": r"^.*foo.*$",
            },
        ]
    )

    # the filetype is recognized given a file path
    assert filetype_map.get_filetype_name(Path("foobar.jpeg")) == "has-foobar"
    assert filetype_map.get_filetype_name(Path("this-foo.jpg")) == "has-foo"

    # check inverse order
    filetype_map = FiletypeMap()
    filetype_map.update(
        [
            {
                "name": "has-foo",
                "regex": r"^.*foo.*$",
            },
            {
                "name": "has-foobar",
                "regex": r"^.*foobar.*$",
            },
        ]
    )

    # the filetype is recognized given a file path
    assert filetype_map.get_filetype_name(Path("foobar.jpeg")) == "has-foo"
    assert filetype_map.get_filetype_name(Path("this-foo.jpg")) == "has-foo"


def test_filetype_overriding():
    # create first version
    filetype_map = FiletypeMap()
    filetype_map.update(
        [
            {
                "name": "one",
                "regex": r"^.*foobar.*$",
            },
            {
                "name": "two",
                "regex": r"^.*foo.*$",
            },
        ]
    )

    # the filetype is recognized given a file path
    assert filetype_map.get_filetype_name(Path("foobar.txt")) == "one"
    assert filetype_map.get_filetype_name(Path("this-foobar.png")) == "one"

    # update
    filetype_map.update(
        [
            {
                "name": "one",
                "regex": r"^.*foobar\.t.*$",
            },
        ]
    )
    assert filetype_map.get_filetype_name(Path("foobar.txt")) == "one"
    assert filetype_map.get_filetype_name(Path("this-foobar.png")) == "two"

    # the regex is correct
    items = [regex for regex in filetype_map.map.values()]
    assert items[0].pattern.pattern == r"^.*foobar\.t.*$"
    assert items[1].pattern.pattern == r"^.*foo.*$"
