
from .frontmatter import parse_frontmatter

def html_extractor(text):
    """Extract data from HTML content into a dictionary.

    The keys of the returned dictionary are:

        :data: metadata coming from an (optional) frontmatter
        :content: the HTML document
        :title: first heading of the HTML document (not yet implemented)
        :toc: list of headings of the HTML document (not yet implemented)

    """

    # parse frontmatter
    content, metadata = parse_frontmatter(text)

    # node info
    # TODO: parse HTML to get title and toc
    node_info = {
        'title': None,
        'data': metadata,
        'toc': None,
        'content': content,
    }
    return node_info

