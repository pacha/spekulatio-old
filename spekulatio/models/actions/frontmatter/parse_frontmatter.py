import re
import yaml

from spekulatio.exceptions import SpekulatioFrontmatterError

FRONTMATTER_PATTERN = re.compile(
    r"^---\s*?^(.*?)^---\s*?^(.*)", re.MULTILINE | re.DOTALL
)


def parse_frontmatter(text):
    """Extract YAML frontmatter data from a text.

    An example of document with frontmatter is::

        ---
        foo: 1
        bar: 2
        ---

        Title
        -----

        Some example text.

    The frontmatter is defined by two lines containing only three dashes ('---'). The first
    one should be the very first line in the document.

    :return: (content, metadata) where metadata is the parsed frontmatter and the document is
        the text without the frontmatter.
    """

    # check if the document has a frontmatter section
    match = FRONTMATTER_PATTERN.fullmatch(text)
    if not match:
        return text, {}

    # get parts
    frontmatter = match.group(1)
    content = match.group(2)

    # parse frontmatter
    try:
        metadata = yaml.safe_load(frontmatter)
    except Exception as err:
        raise SpekulatioFrontmatterError(f"Can't parse YAML in frontmatter: {err}")

    if not isinstance(metadata, dict):
        msg = (
            "The top level YAML element in the frontmatter of a file must be an object."
        )
        raise SpekulatioFrontmatterError(msg)

    return content, metadata
