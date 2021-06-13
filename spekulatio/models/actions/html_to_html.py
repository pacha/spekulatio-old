
from spekulatio.exceptions import SpekulatioReadError

from .templates import render_template
from .templates import render_node_text
from .frontmatter import parse_frontmatter

extension_change = ".html"


def extract_values(node, site):
    """Extract data from HTML file into a dictionary."""

    # create dictionary
    file_content = node.src_path.read_text()
    try:
        src_text, data = parse_frontmatter(file_content)
    except SpekulatioFrontmatterError as err:
        raise SpekulatioReadError(f"{node.src_path}: can't parse frontmatter: {err}")

    # add raw text
    data["_src_text"] = src_text

    return data

def extract_content(node, site):
    """Render the HTML content."""
    # render it
    rendered_content = render_node_text(node, site)

    # return final html content
    content_values = {
        "_content": rendered_content,
    }
    return content_values

def build(src_path, dst_path, node, site):
    """Create page from HTML node."""

    # get content
    content = render_template(node, site)

    # write output file
    dst_path.write_text(content)
