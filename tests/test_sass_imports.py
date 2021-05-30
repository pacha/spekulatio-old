import re
from pathlib import Path

import pytest

from spekulatio.models import Site
from spekulatio.models.filetrees import content_conf
from spekulatio.models.filetrees import template_conf
from spekulatio.exceptions import SpekulatioReadError


def test_value_imports(fixtures_path, tmp_path):

    # source files path
    content_path = fixtures_path / "sass-imports" / "value-imports" / "content"
    templates_path = fixtures_path / "sass-imports" / "value-imports" / "templates"

    # build site
    site = Site(build_path=tmp_path, only_modified=False)
    site.from_directory(templates_path, template_conf)
    site.from_directory(content_path, content_conf)
    site.set_values()
    site.build()

    # check compiled file
    output_path = tmp_path / "styles.css"
    content = output_path.read_text()
    assert content == "a {\n  color: #222222; }\n"


def test_overridden_imports(fixtures_path, tmp_path):

    # source files path
    content_path = fixtures_path / "sass-imports" / "overridden-imports" / "content"
    templates_path = fixtures_path / "sass-imports" / "overridden-imports" / "templates"

    # build site
    site = Site(build_path=tmp_path, only_modified=False)
    site.from_directory(templates_path, template_conf)
    site.from_directory(content_path, content_conf)
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
