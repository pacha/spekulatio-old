
import pytest

from spekulatio.exceptions import SpekulatioError
from spekulatio.som.extractors import json_extractor


def test_extract_json_data():
    """Check basic data extraction."""
    text = """
        {
            "foo": 1,
            "bar": "this"
        }
    """
    node_info = json_extractor(text)
    data = node_info['data']
    assert len(data) == 2
    assert data['foo'] == 1
    assert data['bar'] == "this"


def test_json_non_dict_data():
    """Raise exception if the incoming data is not in dict form."""
    text = """
        [
            "foo",
            "bar"
        ]
    """
    with pytest.raises(SpekulatioError):
        node_info = json_extractor(text)

