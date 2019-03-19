
import pytest

from spekulatio.som.extractors import rst_extractor


def test_extract_rst_data():
    """Check basic data extraction."""
    text = """

:foo: bar
:this: that

Title
=====

This is the body

    """
    data = rst_extractor(text)
    assert len(data) == 3
    assert data['foo'] == "bar"
    assert data['this'] == "that"
    assert 'This is the body' in data['_content']


