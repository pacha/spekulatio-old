
from docutils import io
from docutils import core

from .frontmatter import parse_frontmatter
from spekulatio.exceptions import SpekulatioValueError

extension_change = '.html'

def extract(node):
    """Extract data from RestructuredText file into a dictionary."""

    # create dictionary
    file_content = node.src_path.read_text()
    try:
        src_text, data = parse_frontmatter(file_content)
    except SpekulatioFrontmatterError as err:
        raise SpekulatioReadError(
            f"{node.src_path}: can't parse frontmatter: {err}"
        )

    # add raw text
    data['_src_text'] = src_text

    return data

def build(src_path, dst_path, node, jinja_env, **kwargs):
    """Create page from RestructuredText node."""

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

    # get user settings
    try:
        settings_overrides = node.data['_rst_options']['settings_overrides']
    except KeyError:
        settings_overrides = {}

    try:
        writer_name = node.data['_rst_options']['writer_name']
    except KeyError:
        raise SpekulatioValueError(
            f"{node.src_path}: missing 'writer_name' in '_rst_options'"
        )

    # get source rst text
    src_text = node.data['_src_text']

    # perform rst to html conversion
    output, pub = core.publish_programmatically(
        source_class=io.StringInput, source=src_text,
        source_path=None,
        destination_class=io.NullOutput, destination=None,
        destination_path=None,
        reader=None, reader_name='standalone',
        parser=None, parser_name='restructuredtext',
        writer=None, writer_name=writer_name,
        settings=None, settings_spec=None, settings_overrides=settings_overrides,
        config_section=None, enable_exit_status=None)

    # docinfo is not used for now
    _ = pub.writer.docinfo

    body = pub.writer.parts['html_body']
    toc = _extract_toc(pub.writer.document)

    # update data
    node.data.update({
        '_content': body,
        '_toc': toc,
        '_title': toc[0]['name'] if toc else None,
    })

    # write final html content
    content = node.render_html(jinja_env)
    dst_path.write_text(content)

