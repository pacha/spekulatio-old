import markdown

from .frontmatter import parse_frontmatter
from spekulatio.exceptions import SpekulatioReadError
from spekulatio.exceptions import SpekulatioFrontmatterError

extension_change = ".html"


def extract(node):
    """Extract data from Markdown file into a dictionary."""

    # create dictionary
    file_content = node.src_path.read_text()
    try:
        src_text, data = parse_frontmatter(file_content)
    except SpekulatioFrontmatterError as err:
        raise SpekulatioReadError(f"{node.src_path}: can't parse frontmatter: {err}")

    # add raw text
    data["_src_text"] = src_text

    return data


def post_extract(node):
    """Convert Markdown to HTML."""

    # get extra extensions
    try:
        extensions = node.data["_md_options"]["extensions"]
    except KeyError:
        extensions = ["toc", "fenced_code"]

    # get source rst text
    src_text = node.data["_src_text"]

    # convert text to markdown
    md = markdown.Markdown(extensions=extensions)
    content = md.convert(src_text)

    # get toc
    toc = md.toc_tokens

    node.data.update(
        {
            "_toc": toc,
            "_content": content,
        }
    )


def build(src_path, dst_path, node, jinja_env, **kwargs):
    """Create page from Markdown node."""

    # write final html content
    content = node.render_html(jinja_env)
    dst_path.write_text(content)
