
import pytest
from spekulatio.som.extractors import md_extractor


def test_extract_md_data():
    """Check basic data extraction."""
    text = """---

foo: bar
this: that

---

# Title

This is the body

```python
# python code

def some_func():
    return "nothing"
```
    """
    node_info = md_extractor(text, extra_extensions=['fenced_code'])
    assert node_info['title'] == 'Title'
    assert node_info['toc'] == [{'id': 'title', 'name': 'Title', 'children': [], 'level': 1}]
    assert node_info['data']['foo'] == "bar"
    assert node_info['data']['this'] == "that"
    assert 'This is the body' in node_info['content']
    assert '<code class="language-python">' in node_info['content']  # check for fenced code block
