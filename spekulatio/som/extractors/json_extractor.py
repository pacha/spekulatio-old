
import json

from spekulatio.exceptions import SpekulatioError
from .frontmatter import parse_frontmatter

def json_extractor(text):
    """Extract data from JSON content into a dictionary."""

    # create dictionary
    data = json.loads(text)
    if not isinstance(data, dict):
        msg = "To extract the content, the top level element in a JSON file must be an object"
        raise SpekulatioError(msg)

    return data

