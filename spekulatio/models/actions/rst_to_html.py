from docutils import io
from docutils import core

from spekulatio.exceptions import SpekulatioValueError

from .templates import render_template
from .templates import render_node_text
from .frontmatter import parse_frontmatter

extension_change = ".html"


def extract_values(node, site):
    """Extract data from RestructuredText file into a dictionary."""

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
    """Set values after parsing the RestructuredText content."""

    # render it
    rendered_content = render_node_text(node, site)

    def _extract_toc(node, level=1, toc_depth=3):
        """Extract table of contents from rst document."""
        # check if this level has to be processed
        if level > toc_depth:
            return []

        # create toc entries for this level
        entries = [
            {
                "level": level,
                "id": child.attributes.get("ids", [""])[0],
                "name": child.children[0].astext(),
                "children": _extract_toc(child, level + 1, toc_depth),
            }
            for child in node.children
            if child.tagname == "section"
        ]

        return entries

    # default rst conversion options
    rst_options = {
        "settings_overrides": {
            "doctitle_xform": False,
            "initial_header_level": 1,
        },
        "writer_name": "html5",
    }
    if "_rst_options" in node.data:
        rst.options.update(node.data["_rst_options"])
    settings_overrides = rst_options["settings_overrides"]
    writer_name = rst_options["writer_name"]

    # perform rst to html conversion
    output, pub = core.publish_programmatically(
        source_class=io.StringInput,
        source=rendered_content,
        source_path=None,
        destination_class=io.NullOutput,
        destination=None,
        destination_path=None,
        reader=None,
        reader_name="standalone",
        parser=None,
        parser_name="restructuredtext",
        writer=None,
        writer_name=writer_name,
        settings=None,
        settings_spec=None,
        settings_overrides=settings_overrides,
        config_section=None,
        enable_exit_status=None,
    )

    # docinfo is not used for now
    _ = pub.writer.docinfo

    body = pub.writer.parts["html_body"]
    toc = _extract_toc(pub.writer.document)

    # update data
    content_values = {
        "_content": body,
        "_toc": toc,
    }

    return content_values

def build(src_path, dst_path, node, site):
    """Create page from RestructuredText node."""

    # get content
    content = render_template(node, site)

    # write output file
    dst_path.write_text(content)
