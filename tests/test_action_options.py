import re
from pathlib import Path

import pytest

from spekulatio.models import Site
from spekulatio.models.input_dirs import InputDir
from spekulatio.paths import default_input_dir_path
from spekulatio.exceptions import SpekulatioReadError


def test_md_options(fixtures_path, tmp_path):

    # input dirs
    default_dir = InputDir(default_input_dir_path, "site_templates")
    content_path = fixtures_path / "action-options" / "md-options" / "content"
    content_dir = InputDir(content_path, "site_content")

    # build site
    site = Site(output_path=tmp_path, only_modified=False)
    site.from_directory(default_dir)
    site.from_directory(content_dir)
    site.set_values()
    site.render_content()
    site.build()

    # get output content
    output_path = tmp_path / "foo.html"
    content = output_path.read_text()
    remove_whitespace = r"(\ \ +)|\n"
    minimized_content = re.sub(remove_whitespace, "", content)

    assert (
        minimized_content
        == '<div class="admonition note"><p class="admonition-title">Note</p></div>'
    )


def test_sass_options(fixtures_path, tmp_path):

    # input dirs
    default_dir = InputDir(default_input_dir_path, "site_templates")
    content_path = fixtures_path / "action-options" / "sass-options" / "content"
    content_dir = InputDir(content_path, "site_content")

    # build site
    site = Site(output_path=tmp_path, only_modified=False)
    site.from_directory(default_dir)
    site.from_directory(content_dir)
    site.set_values()
    site.build()

    # get output content
    output_path = tmp_path / "foo.css"
    content = output_path.read_text()
    remove_whitespace = r"(\ \ +)|\n"
    minimized_content = re.sub(remove_whitespace, "", content)

    assert minimized_content == ".alert {border: 1px solid rgba(198, 83, 140, 0.88); }"
