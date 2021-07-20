import re
from pathlib import Path

import pytest

from spekulatio.models import Site
from spekulatio.models import InputDir
from spekulatio.models import ActionMap
from spekulatio.models import all_actions
from spekulatio.models import default_filetype_map
from spekulatio.exceptions import SpekulatioReadError


def test_no_actions(fixtures_path, tmp_path):

    # source files path
    content_path = fixtures_path / "action-maps" / "no-actions" / "content"
    content_dir = InputDir(
        path=content_path,
        preset_name=None,
        action_dicts=[],
    )

    # build site
    site = Site(output_path=tmp_path, only_modified=False)
    site.from_directory(content_dir)
    site.set_values()
    site.render_content()
    site.build()

    # list files
    assert not list(tmp_path.iterdir())


def test_action_map_empty():

    action_map = ActionMap(default_filetype_map)

    assert action_map.get_action(Path("foo/bar.json")) == all_actions["ignore"]
    assert action_map.get_action(Path("foo/bar.html")) == all_actions["ignore"]
    assert action_map.get_action(Path("foo/bar.yaml")) == all_actions["ignore"]


def test_action_map_one_action():

    action_map = ActionMap(default_filetype_map)
    action_map.update_actions(
        [
            {
                "filetype": "html",
                "action": "use_as_template",
            },
        ]
    )

    assert action_map.get_action(Path("foo/bar.json")) == all_actions["ignore"]
    assert action_map.get_action(Path("foo/bar.html")) == all_actions["use_as_template"]
    assert action_map.get_action(Path("foo/bar.yaml")) == all_actions["ignore"]


def test_action_map_two_actions():

    action_map = ActionMap(default_filetype_map)
    action_map.update_actions(
        [
            {
                "filetype": "html",
                "action": "use_as_template",
            },
            {
                "filetype": "json",
                "action": "copy",
            },
        ]
    )

    assert action_map.get_action(Path("foo/bar.json")) == all_actions["copy"]
    assert action_map.get_action(Path("foo/bar.html")) == all_actions["use_as_template"]
    assert action_map.get_action(Path("foo/bar.yaml")) == all_actions["ignore"]


def test_action_map_default_action():

    action_map = ActionMap(default_filetype_map)
    action_map.update_actions(
        [
            {
                "filetype": "html",
                "action": "use_as_template",
            },
        ]
    )
    action_map.update_default_action("render")

    assert action_map.get_action(Path("foo/bar.json")) == all_actions["render"]
    assert action_map.get_action(Path("foo/bar.html")) == all_actions["use_as_template"]
    assert action_map.get_action(Path("foo/bar.yaml")) == all_actions["render"]
