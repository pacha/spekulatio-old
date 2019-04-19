
import yaml

from spekulatio.exceptions import SpekulatioError
from .frontmatter import parse_frontmatter

def yaml_extractor(text):
    """Extract data from YAML content into a dictionary."""

    # create dictionary
    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        msg = "To extract the content, the top level element in a YAML file must be an object"
        raise SpekulatioError(msg)

    return data

