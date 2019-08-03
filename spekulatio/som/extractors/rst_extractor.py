
from docutils import io
from docutils import core

from .frontmatter import parse_frontmatter

def rst_extractor(text):
    """Extract data from RestructuredText content into a dictionary.

    The keys of the dictionary are:

        :data: metadata coming from an (optional) frontmatter and (optional) docinfo sections.
        :content: the HTML document generated from the RestructuredText one
        :title: first heading of the document
        :toc: list of headings of document

    The docinfo section of a RestructuredText file is a definition list at the
    very start of the document. Eg::

        :author: Me
        :field: value

        Title
        =====
        ...

    Both the frontmatter and the docinfo can be present simultaneously in the
    same file. If that's the case, frontmatter items have preference over the
    docinfo ones if the keys are the same. (Be also aware than in the
    docinfo section the values can't have a type other than strings, unlike
    in frontmatter).
    """

    # parse frontmatter
    content, metadata = parse_frontmatter(text)

    settings_overrides = {
        'doctitle_xform': False,
        'initial_header_level': 1,
    }

    output, pub = core.publish_programmatically(
        source_class=io.StringInput, source=content,
        source_path=None,
        destination_class=io.NullOutput, destination=None,
        destination_path=None,
        reader=None, reader_name='standalone',
        parser=None, parser_name='restructuredtext',
        writer=None, writer_name='html5',
        settings=None, settings_spec=None, settings_overrides=settings_overrides,
        config_section=None, enable_exit_status=None)

    docinfo = pub.writer.docinfo
    body = pub.writer.parts['html_body']
    toc = _extract_toc(pub.writer.document)

    data = {}
    data.update(docinfo)
    data.update(metadata)

    # create dictionary
    node_info = {
        'title': toc[0]['name'] if toc else None,
        'data': data,
        'toc': toc,
        'content': body,
    }
    return node_info

def _extract_toc(node, level=1, toc_depth=3):
    """Extract table of contents from rst document."""
    # check if this level has to be processed
    if level > toc_depth:
        return []

    # create toc entries for this level
    entries = [
        {
            'level': level,
            'id': child.attributes.get('ids', [''])[0],
            'name': child.children[0].astext(),
            'children': _extract_toc(child, level + 1, toc_depth)
        }
        for child in node.children if child.tagname == 'section'
    ]

    return entries

