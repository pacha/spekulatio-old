
from docutils import io
from docutils import core
from rst2html5_ import HTML5Writer

from .frontmatter import parse_frontmatter

def rst_extractor(text):
    """Extract data from RestructuredText content into a dictionary.

    The keys of the dictionary are:

        * the metadata coming from an (optional) frontmatter

        * the metadata coming from an (optional) docinfo section

        * the '_content' key containing the document converted to HTML

        * the '_toc' key containing the document's table of contents

    The docinfo section of a RestructuredText file is a definition list at the
    very start of the document. Eg::

        :author: Me
        :field: value

        Title
        =====
        ...

    Both the frontmatter and the docinfo can be present simultaneously in the
    same file. If that's the case, docinfo items have preference over the
    frontmatter ones if the keys are the same. (Be also aware than in the
    docinfo section the values can't have a type other than strings, unlike
    in frontmatter).
    """

    # parse frontmatter
    content, metadata = parse_frontmatter(text)

    # parse content
    output, pub = core.publish_programmatically(
        source_class=io.StringInput, source=content,
        source_path=None,
        destination_class=io.NullOutput, destination=None,
        destination_path=None,
        reader=None, reader_name='standalone',
        parser=None, parser_name='restructuredtext',
        writer=HTML5Writer(), writer_name='null',
        settings=None, settings_spec=None, settings_overrides=None,
        config_section=None, enable_exit_status=None)

    docinfo = pub.writer.docinfo
    body = pub.writer.body
    toc = _extract_toc(pub.writer.document)

    # create dictionary
    data = {}
    data.update(metadata)
    data.update(docinfo)
    data['_content'] = body
    data['_toc'] = toc

    return data

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

