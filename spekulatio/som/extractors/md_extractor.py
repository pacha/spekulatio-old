
import markdown

from .frontmatter import parse_frontmatter

def md_extractor(text):
    """Extract data from Markdown content into a dictionary.

    The keys of the dictionary are:

        :data: metadata coming from an (optional) frontmatter.
        :content: the HTML document generated from the Markdown one
        :title: first heading of the document
        :toc: list of headings of document
    """

    # parse frontmatter
    content, data = parse_frontmatter(text)

    # get body and toc
    md = markdown.Markdown(extensions=['toc'])
    body = md.convert(content)
    toc = md.toc_tokens

    # create dictionary
    node_info = {
        'title': toc[0]['name'] if toc else None,
        'data': data,
        'toc': toc,
        'content': body,
    }
    return node_info

