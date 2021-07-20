from spekulatio.exceptions import SpekulatioReadError

from .templates import render_template
from .templates import render_node_text
from .frontmatter import parse_frontmatter

extension_change = None


def extract_values(node, site):
    """Extract data from file into a dictionary."""

    # add raw text
    data["_src_text"] = node.src_path.read_text()

    return data


def extract_content(node, site):
    """Render content."""
    # render it
    rendered_content = render_node_text(node, site)

    # return final html content
    content_values = {
        "_content": rendered_content,
    }
    return content_values


def build(src_path, dst_path, node, site):
    """Create page from node."""

    # get content
    content = node.data["_content"]

    # write output file
    dst_path.write_text(content)
