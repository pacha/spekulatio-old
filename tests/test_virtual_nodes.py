import re
from pathlib import Path

import pytest

from spekulatio.models import Site
from spekulatio.models.filetrees import content_conf
from spekulatio.models.filetrees import template_conf
from spekulatio.exceptions import SpekulatioReadError


def test_virtual_node_creation(fixtures_path, tmp_path):

    # source files path
    content_path = fixtures_path / "virtual-nodes" / "creation" / "content"
    current_path = Path(__file__).absolute().parent.parent
    default_template_path = (
        current_path / "data" / "template-dirs" / "spekulatio-default"
    )

    site = Site(build_path=tmp_path, only_modified=False)
    site.from_directory(default_template_path, template_conf)
    site.from_directory(content_path, content_conf)
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
