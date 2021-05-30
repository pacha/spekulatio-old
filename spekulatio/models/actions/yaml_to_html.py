
import yaml

from spekulatio.exceptions import SpekulatioBuildError

extension_change = '.html'

def extract(node):
    """Extract data from YAML content into a dictionary."""

    # create dictionary
    with node.src_path.open() as fd:
        data = yaml.safe_load(fd)
    if not isinstance(data, dict):
        msg = "To extract the content, the top level element in a YAML file must be an object"
        raise SpekulatioBuildError(msg)
    return data

def build(src_path, dst_path, node, jinja_env, **kwargs):
    """Create page from YAML file."""
    content = node.render_html(jinja_env)
    dst_path.write_text(content)

