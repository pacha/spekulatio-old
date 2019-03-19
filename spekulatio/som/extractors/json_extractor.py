
import json

from spekulatio.exceptions import SpekulatioError

def json_extractor(text):
    """Extract data from JSON content"""
    data = json.loads(text)
    if not isinstance(data, dict):
        msg = "To extract the content, the top level element in a JSON file must be an object"
        raise SpekulatioError(msg)
    return data

