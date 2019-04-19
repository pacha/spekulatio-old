
from .frontmatter import parse_frontmatter

def html_extractor(text):
    """Extract data from HTML content into a dictionary.

    The keys of the returned dictionary are:

        * metadata coming from an (optional) frontmatter

        * the '_content' key containing the HTML document

    """

    # parse frontmatter
    content, metadata = parse_frontmatter(text)

    # create dictionary
    data = {}
    data.update(metadata)
    data['_content'] = content

    return data

