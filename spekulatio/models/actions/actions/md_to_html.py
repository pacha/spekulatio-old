import logging

import markdown

from spekulatio.exceptions import SpekulatioReadError
from spekulatio.exceptions import SpekulatioWriteError
from spekulatio.exceptions import SpekulatioFrontmatterError
from .templates import render_template
from .templates import render_node_text
from .frontmatter import parse_frontmatter

extension_change = ".html"

# disable debug messages from markdown module
markdown_logger = logging.getLogger("MARKDOWN")
markdown_logger.setLevel(logging.ERROR)


def extract_values(node, site):
    """Extract data from Markdown file into a dictionary."""

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
    """Convert Markdown to HTML."""

    # render it
    rendered_content = render_node_text(node, site)

    # get extra extensions
    try:
        extensions = node.data["_md_options"]["extensions"]
    except KeyError:
        extensions = ["toc", "fenced_code", "admonition", "attr_list", "def_list"]

    # convert text to markdown
    md = markdown.Markdown(extensions=extensions)
    content = md.convert(rendered_content)

    # get toc
    toc = md.toc_tokens

    content_values = {
        "_toc": toc,
        "_content": content,
    }

    return content_values


def build(src_path, dst_path, node, site):
    """Create page from Markdown node."""

    # get content
    content = render_template(node, site)

    # write output file
    dst_path.write_text(content)
