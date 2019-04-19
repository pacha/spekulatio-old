
from rst2html5_ import HTML5Writer
from docutils.core import publish_parts

from .frontmatter import parse_frontmatter

def rst_extractor(text):
    """Extract data from RestructuredText content into a dictionary.

    The keys of the dictionary are:

        * the metadata coming from an (optional) frontmatter

        * the metadata coming from an (optional) docinfo section

        * the '_content' key containing the document converted to HTML

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

    # parse docinfo
    parts = publish_parts(writer=HTML5Writer(), source=content)
    docinfo = parts['docinfo']
    body = parts['body']

    # create dictionary
    data = {}
    data.update(metadata)
    data.update(docinfo)
    data['_content'] = body

    return data

