
import yaml

from spekulatio.exceptions import SpekulatioBuildError

extension_change = None

def extract(node):
    """Treat virtual node as a normal YAML file when it comes to extract values."""

    # create dictionary
    with node.src_path.open() as fd:
        data = yaml.safe_load(fd)
    if not isinstance(data, dict):
        msg = "To extract the content, the top level element in a YAML file must be an object"
        raise SpekulatioBuildError(msg)
    return data

def build(src_path, dst_path, node, **kwargs):
    """Virtual nodes don't generate any output."""
    pass

