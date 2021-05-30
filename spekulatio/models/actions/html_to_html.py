
from .frontmatter import parse_frontmatter
from spekulatio.exceptions import SpekulatioReadError

extension_change = '.html'

def extract(node):
    """Extract data from HTML file into a dictionary."""

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

def post_extract(node):
    """Set special variables."""
    # write final html content
    src_text = node.data['_src_text']
    node.data.update({
        '_content': src_text,
    })

def build(src_path, dst_path, node, jinja_env, **kwargs):
    """Create page from HTML node."""
    content = node.render_html(jinja_env)
    dst_path.write_text(content)

