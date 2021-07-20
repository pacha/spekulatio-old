import re
from pathlib import Path

import pytest

from spekulatio.models import Site
from spekulatio.models.input_dirs import InputDir
from spekulatio.paths import default_input_dir_path
from spekulatio.exceptions import SpekulatioReadError


def test_overriding_templates(fixtures_path, tmp_path):

    # source files path
    templates1_path = fixtures_path / "templates" / "overriding" / "templates1"
    templates1_dir = InputDir(templates1_path, "site_templates")
    templates2_path = fixtures_path / "templates" / "overriding" / "templates2"
    templates2_dir = InputDir(templates2_path, "site_templates")
    content_path = fixtures_path / "templates" / "overriding" / "content"
    content_dir = InputDir(content_path, "site_content")

    # build site
    site = Site(output_path=tmp_path, only_modified=False)
    site.from_directory(templates1_dir)
    site.from_directory(templates2_dir)
    site.from_directory(content_dir)
    site.set_values()
    site.build()

    # check a
    output_path = tmp_path / "a.html"
    a_content = output_path.read_text()
    assert a_content == "foo in template2 | name: a"

    # check b
    output_path = tmp_path / "b.html"
    b_content = output_path.read_text()
    assert b_content == "bar in template1 | name: b"

    # check c
    output_path = tmp_path / "c.html"
    c_content = output_path.read_text()
    assert c_content == "baz in template2 | name: c"
