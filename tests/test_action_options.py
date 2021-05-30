
import re
from pathlib import Path

import pytest

from spekulatio.models import Site
from spekulatio.models.filetrees import content_conf
from spekulatio.models.filetrees import template_conf
from spekulatio.exceptions import SpekulatioReadError


def test_md_options(fixtures_path, tmp_path):

    # source files path
    content_path = fixtures_path / 'action-options' / 'md-options' / 'content'
    current_path = Path(__file__).absolute().parent.parent
    default_template_path = current_path / 'data' / "template-dirs" / "spekulatio-default"

    # build site
    site = Site(build_path=tmp_path, only_modified=False)
    site.from_directory(default_template_path, template_conf)
    site.from_directory(content_path, content_conf)
    site.set_values()
    site.build()

    # get output content
    output_path = tmp_path / 'foo.html'
    content = output_path.read_text()
    remove_whitespace = r"(\ \ +)|\n"
    minimized_content = re.sub(remove_whitespace, "", content)

    assert minimized_content == '<div class="admonition note"><p class="admonition-title">Note</p></div>'

def test_sass_options(fixtures_path, tmp_path):

    # source files path
    content_path = fixtures_path / 'action-options' / 'sass-options' / 'content'

    # build site
    site = Site(build_path=tmp_path, only_modified=False)
    site.from_directory(content_path, content_conf)
    site.set_values()
    site.build()

    # get output content
    output_path = tmp_path / 'foo.css'
    content = output_path.read_text()
    remove_whitespace = r"(\ \ +)|\n"
    minimized_content = re.sub(remove_whitespace, "", content)

    assert minimized_content == '.alert {border: 1px solid rgba(198, 83, 140, 0.88); }'

