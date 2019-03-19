
import yaml

from spekulatio.exceptions import SpekulatioError

def yaml_extractor(text):
    """Extract data from YAML content"""
    data = yaml.load(text)
    if not isinstance(data, dict):
        msg = "To extract the content, the top level element in a YAML file must be an object"
        raise SpekulatioError(msg)
    return data

