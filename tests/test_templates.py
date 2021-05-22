
import re
from pathlib import Path

import pytest

from spekulatio.models import Site
from spekulatio.models.filetrees import content_conf
from spekulatio.models.filetrees import template_conf
from spekulatio.exceptions import SpekulatioReadError


def test_overriding_templates(fixtures_path, tmp_path):

    # source files path
    content_path = fixtures_path / 'templates' / 'overriding' / 'content'
    templates1_path = fixtures_path / 'templates' / 'overriding' / 'templates1'
    templates2_path = fixtures_path / 'templates' / 'overriding' / 'templates2'

    # build site
    site = Site(build_path=tmp_path, only_modified=False)
    site.from_directory(templates1_path, template_conf)
    site.from_directory(templates2_path, template_conf)
    site.from_directory(content_path, content_conf)
    site.build()

    # check a
    output_path = tmp_path / 'a.html'
    a_content = output_path.read_text()
    assert a_content == 'foo in template2 | name: a'

    # check b
    output_path = tmp_path / 'b.html'
    b_content = output_path.read_text()
    assert b_content == 'bar in template1 | name: b'

    # check c
    output_path = tmp_path / 'c.html'
    c_content = output_path.read_text()
    assert c_content == 'baz in template2 | name: c'

