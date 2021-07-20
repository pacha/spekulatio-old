import re
from pathlib import Path

import pytest

from spekulatio.models import Site
from spekulatio.models.input_dirs import InputDir
from spekulatio.paths import default_input_dir_path
from spekulatio.exceptions import SpekulatioReadError


def test_virtual_node_creation(fixtures_path, tmp_path):

    # source files path
    default_dir = InputDir(default_input_dir_path, "site_templates")
    content_path = fixtures_path / "virtual-nodes" / "creation" / "content"
    content_dir = InputDir(content_path, "site_content")

    site = Site(output_path=tmp_path, only_modified=False)
    site.from_directory(default_dir)
    site.from_directory(content_dir)
    site.set_values()
    site.build()

    # the virtual node is not generated but the normal one is
    output_path = tmp_path / "foo.meta.html"
    assert not output_path.exists()
    output_path = tmp_path / "foo.html"
    assert output_path.exists()

    # the virtual node is present in site.nodes, but with its relative src path
    assert "/foo.meta.yaml" in site.nodes
    assert "/foo.meta.html" not in site.nodes
    assert "/foo.html" in site.nodes

    # the node handles values like a normal node
    virtual_node = site.nodes["/foo.meta.yaml"]
    assert virtual_node.data["bar"] == 3
