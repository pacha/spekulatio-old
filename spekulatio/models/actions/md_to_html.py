
import markdown

from .frontmatter import parse_frontmatter
from spekulatio.exceptions import SpekulatioReadError
from spekulatio.exceptions import SpekulatioFrontmatterError

extension_change = '.html'

def extract(node):
    """Extract data from Markdown file into a dictionary."""

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
    """Create page from Markdown node."""

    # get extra extensions
    try:
        extensions = node.local_data['_md_options']['extensions']
    except KeyError:
        extensions = []

    # get source rst text
    src_text = node.data['_src_text']

    # convert text to markdown
    md = markdown.Markdown(extensions=extensions)
    content = md.convert(src_text)
    toc = md.toc_tokens
    node.local_data.update({
        '_content': content,
        '_toc': toc,
        '_title': toc[0]["name"] if toc else None,
    })

    # write final html content
    content = node.render_html(jinja_env)
    dst_path.write_text(content)

