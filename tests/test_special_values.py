from pathlib import Path

import pytest

from spekulatio.models import Site
from spekulatio.models.input_dirs import InputDir
from spekulatio.paths import default_input_dir_path
from spekulatio.exceptions import SpekulatioReadError


def test_title(fixtures_path, tmp_path):

    # source files path
    templates_path = fixtures_path / "special-values" / "title" / "templates"
    templates_dir = InputDir(templates_path, "site_templates")
    content_path = fixtures_path / "special-values" / "title" / "content"
    content_dir = InputDir(content_path, "site_content")

    # build site
    site = Site(output_path=tmp_path, only_modified=False)
    site.from_directory(templates_dir)
    site.from_directory(content_dir)
    site.set_values()
    site.render_content()
    site.build()

    output_path = tmp_path / "empty.html"
    assert output_path.read_text() == "/empty.html|/empty.html"

    output_path = tmp_path / "from-text.html"
    assert output_path.read_text() == "from-text|from-text"

    output_path = tmp_path / "overwritten.html"
    assert output_path.read_text() == "overwritten-title|overwritten-title"


def test_alias(fixtures_path, tmp_path):

    # source files path
    templates_path = fixtures_path / "special-values" / "alias" / "templates"
    templates_dir = InputDir(templates_path, "site_templates")
    content_path = fixtures_path / "special-values" / "alias" / "content"
    content_dir = InputDir(content_path, "site_content")

    # build site
    site = Site(output_path=tmp_path, only_modified=False)
    site.from_directory(templates_dir)
    site.from_directory(content_dir)
    site.set_values()
    site.set_relationships()

    # site.display_tree()
    site.build()

    output_path = tmp_path / "foo.html"
    assert output_path.read_text() == "foo.html"

    output_path = tmp_path / "bar.html"
    assert output_path.read_text() == "foo.html"


def test_url(fixtures_path, tmp_path):

    # source files path
    templates_path = fixtures_path / "special-values" / "url" / "templates"
    templates_dir = InputDir(templates_path, "site_templates")
    content_path = fixtures_path / "special-values" / "url" / "content"
    content_dir = InputDir(content_path, "site_content")

    # build site
    site = Site(output_path=tmp_path, only_modified=False)
    site.from_directory(templates_dir)
    site.from_directory(content_dir)
    site.set_values()
    site.build()

    output_path = tmp_path / "foo.html"
    assert output_path.read_text() == "/made-up.html|/made-up.html"

    # site.nodes should not contain overwritten urls
    assert "/foo.html" in site.nodes
    assert "/made-up.html" not in site.nodes

    output_path = tmp_path / "bar.html"
    assert output_path.read_text() == "/bar.html|/bar.html"
