import re
from pathlib import Path

import pytest

from spekulatio.models import Site
from spekulatio.models import InputDir
from spekulatio.models import FiletypeMap
from spekulatio.models import filetype_presets
from spekulatio.paths import default_input_dir_path
from spekulatio.exceptions import SpekulatioReadError


@pytest.fixture(
    scope="function",
    params=[
        "html-to-html",
        "md-to-html",
        "rst-to-html",
        "json-to-html",
        "yaml-to-html",
    ],
)
def html_render_action(request):
    yield request.param


@pytest.fixture(scope="function", params=["sass-to-css", "scss-to-css"])
def css_render_action(request):
    yield request.param


def test_copy_action(fixtures_path, tmp_path):

    # input dirs
    content_path = fixtures_path / "actions" / "copy" / "content"
    content_dir = InputDir(content_path, "site_content")

    site = Site(output_path=tmp_path, only_modified=False)
    site.from_directory(content_dir)
    site.build()

    output_path = tmp_path / "foo.txt"
    assert output_path.read_text() == "just some content\n"


def test_create_dir_action(fixtures_path, tmp_path):

    # input dirs
    content_path = fixtures_path / "actions" / "create-dir" / "content"
    content_dir = InputDir(content_path, "site_content")

    site = Site(output_path=tmp_path, only_modified=False)
    site.from_directory(content_dir)
    site.build()

    output_path = tmp_path / "dir1" / "foo.txt"
    assert output_path.read_text() == "just some content\n"


def test_render_html_action(fixtures_path, tmp_path, html_render_action):

    # source files path
    content_path = fixtures_path / "actions" / html_render_action / "content"
    content_dir = InputDir(content_path, "site_content")
    default_dir = InputDir(default_input_dir_path, "site_templates")

    # build site
    site = Site(output_path=tmp_path, only_modified=False)
    site.from_directory(default_dir)
    site.from_directory(content_dir)
    site.set_values()
    site.render_content()
    site.build()

    # text extractor
    node = site.nodes["/foo.html"]
    assert node.user_data == {"my_var": 200}

    # get output content
    output_path = tmp_path / "foo.html"
    content = output_path.read_text()
    remove_whitespace = r"(\ \ +)|\n"
    minimized_content = re.sub(remove_whitespace, "", content)

    # get expected output
    expected_start = '<!DOCTYPE html><html><head><meta charset="UTF-8">'
    partial_content = "<p>Some text</p>"
    expected_end = "</body></html>"

    assert minimized_content.startswith(expected_start)
    assert partial_content in minimized_content
    assert minimized_content.endswith(expected_end)


def test_css_render_action(fixtures_path, tmp_path, css_render_action):

    # source files path
    content_path = fixtures_path / "actions" / css_render_action / "content"
    content_dir = InputDir(content_path, "site_content")

    # build site
    site = Site(output_path=tmp_path, only_modified=False)
    site.from_directory(content_dir)
    site.build()

    # get output content
    output_path = tmp_path / "foo.css"
    content = output_path.read_text()
    remove_whitespace = r"(\ \ +)|\n"
    minimized_content = re.sub(remove_whitespace, "", content)

    assert minimized_content == ".alert {border: 1px solid rgba(198, 83, 140, 0.88); }"


def test_render_action(fixtures_path, tmp_path):

    # set filetype map
    filetype_map = FiletypeMap()
    filetype_map.update(filetype_presets)
    filetype_map.update(
        [
            {
                "name": "txt",
                "extensions": [".txt"],
            }
        ]
    )

    # source files path
    content_path = fixtures_path / "actions" / "render" / "content"
    content_dir = InputDir(
        path=content_path,
        preset_name="site_content",
        filetype_map=filetype_map,
        action_dicts=[
            {
                "filetype": "txt",
                "action": "render",
            }
        ],
    )

    # build site
    site = Site(output_path=tmp_path, only_modified=False)
    site.from_directory(content_dir)
    site.set_values()
    site.render_content()
    site.build()

    # text extractor
    node = site.nodes["/foo.txt"]
    assert node.user_data == {"my_var": 200}

    # get output content
    output_path = tmp_path / "foo.txt"
    content = output_path.read_text()

    assert content.strip() == "The amount is 200."


def test_render_without_frontmatter_action(fixtures_path, tmp_path):

    # set filetype map
    filetype_map = FiletypeMap()
    filetype_map.update(filetype_presets)
    filetype_map.update(
        [
            {
                "name": "txt",
                "extensions": [".txt"],
            }
        ]
    )

    # source files path
    content_path = fixtures_path / "actions" / "render-without-frontmatter" / "content"
    content_dir = InputDir(
        path=content_path,
        preset_name="site_content",
        filetype_map=filetype_map,
        action_dicts=[
            {
                "filetype": "txt",
                "action": "render",
            }
        ],
    )

    # build site
    site = Site(output_path=tmp_path, only_modified=False)
    site.from_directory(content_dir)
    site.set_values()
    site.render_content()
    site.build()

    # get output content
    output_path = tmp_path / "foo.txt"
    content = output_path.read_text()

    assert content.strip() == "The amount is 200."
