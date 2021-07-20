import yaml

from spekulatio.exceptions import SpekulatioWriteError

extension_change = None


def extract_values(node, site):
    """Treat virtual node as a normal YAML file when it comes to extract values."""

    # create dictionary
    with node.src_path.open() as fd:
        data = yaml.safe_load(fd)
    if not isinstance(data, dict):
        msg = "To extract the content, the top level element in a YAML file must be an object"
        raise SpekulatioWriteError(msg)
    return data


def extract_content(node, site):
    return {}


def build(src_path, dst_path, node, site):
    """Virtual nodes don't generate any output."""
    pass
