
import pytest

from spekulatio.exceptions import SpekulatioError
from spekulatio.som.extractors import yaml_extractor


def test_extract_yaml_data():
    """Check basic data extraction."""
    text = """
        foo: 1
        bar: value
        bat:
          - one
          - two
    """
    node_info = yaml_extractor(text)
    data = node_info['data']
    assert len(data) == 3
    assert data['foo'] == 1
    assert data['bar'] == 'value'
    assert data['bat'] == ['one', 'two']


def test_json_non_dict_data():
    """Raise exception if the incoming data is not in dict form."""
    text = """
        [
            "foo",
            "bar"
        ]
    """
    with pytest.raises(SpekulatioError):
        data = yaml_extractor(text)

