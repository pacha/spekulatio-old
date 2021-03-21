
from spekulatio.model.frontmatter import parse_frontmatter


def test_parse_frontmatter():
    """Check basic data extraction."""
    text = """---
foo: bar
this: that
---
content."""

    document, metadata = parse_frontmatter(text)
    assert metadata == {'foo': 'bar', 'this': 'that'}
    assert document == "content."

