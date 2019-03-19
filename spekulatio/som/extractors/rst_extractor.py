
from collections import OrderedDict

from rst2html5_ import HTML5Writer
from docutils.core import publish_parts


def rst_extractor(text):
    """Extract data from RestructuredText content.

    The docinfo section of a rst file is a definition list at the
    very start of the document. Eg::

        :author: Me
        :field: value

        Title
        =====
        ...

    The returned data is a dictionary that contains all the items
    in the docinfo section plus an additional '_content' entry whose
    value is the rst document rendered as HTML.
    """
    parts = publish_parts(writer=HTML5Writer(), source=text)
    data = OrderedDict()
    data.update(parts['docinfo'])
    data['_content'] = parts['body']
    return data

