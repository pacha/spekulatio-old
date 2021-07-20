import re
from pathlib import Path

import pytest

from spekulatio.models import Site
from spekulatio.models.input_dirs import InputDir
from spekulatio.paths import default_input_dir_path
from spekulatio.exceptions import SpekulatioReadError


def test_value_imports(fixtures_path, tmp_path):

    # source files path
    templates_path = fixtures_path / "sass-imports" / "value-imports" / "templates"
    templates_dir = InputDir(templates_path, "site_templates")
    content_path = fixtures_path / "sass-imports" / "value-imports" / "content"
    content_dir = InputDir(content_path, "site_content")

    # build site
    site = Site(output_path=tmp_path, only_modified=False)
    site.from_directory(templates_dir)
    site.from_directory(content_dir)
    site.set_values()
    site.build()

    # check compiled file
    output_path = tmp_path / "styles.css"
    content = output_path.read_text()
    assert content == "a {\n  color: #222222; }\n"


def test_overridden_imports(fixtures_path, tmp_path):

    # source files path
    templates_path = fixtures_path / "sass-imports" / "overridden-imports" / "templates"
    templates_dir = InputDir(templates_path, "site_templates")
    content_path = fixtures_path / "sass-imports" / "overridden-imports" / "content"
    content_dir = InputDir(content_path, "site_content")

    # build site
    site = Site(output_path=tmp_path, only_modified=False)
    site.from_directory(templates_dir)
    site.from_directory(content_dir)
    site.set_values()
    site.build()

    # check compiled file
    output_path = tmp_path / "styles.css"
    content = output_path.read_text()
    assert content == "a {\n  color: #222222; }\n"

    # check second compiled file
    output_path = tmp_path / "foo" / "bar" / "baz" / "other.css"
    content = output_path.read_text()
    assert content == "a {\n  color: #222222; }\n"
