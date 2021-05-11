
import json

from spekulatio.exceptions import SpekulatioBuildError

extension_change = '.html'

def extract(node):
    """Extract data from JSON content into a dictionary."""

    # create dictionary
    with node.src_path.open() as fd:
        data = json.loads(fd)
    if not isinstance(data, dict):
        msg = "To extract the content, the top level element in a JSON file must be an object"
        raise SpekulatioBuildError(msg)
    return data

def build(src_path, dst_path, node, jinja_env, **kwargs):
    """Create page from JSON file."""
    content = node.render_html(jinja_env)
    dst_path.write_text(content)

