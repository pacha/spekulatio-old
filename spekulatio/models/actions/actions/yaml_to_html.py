import yaml

from spekulatio.exceptions import SpekulatioWriteError

from .templates import render_template

extension_change = ".html"


def extract_values(node, site):
    """Extract data from YAML content into a dictionary."""

    # create dictionary
    with node.src_path.open() as fd:
        data = yaml.safe_load(fd)
    if not isinstance(data, dict):
        msg = "To extract the content, the top level element in a YAML block must be an object"
        raise SpekulatioWriteError(msg)
    return data


def extract_content(node, site):
    return {}


def build(src_path, dst_path, node, site):
    """Create page from YAML file."""

    # get content
    content = render_template(node, site)

    # write output file
    dst_path.write_text(content)
