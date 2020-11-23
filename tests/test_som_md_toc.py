
import pytest

from spekulatio.som.extractors import md_extractor


def test_extract_rst_data():
    """Check basic data extraction."""
    text = """
# Title One

text of title one

## Title Two

text of title two

### Title Three

text of title three

## Title Four

text of title four

    """
    node_info = md_extractor(text)
    assert node_info['toc'] == [
        {
            'level': 1,
            'id': 'title-one',
            'name': 'Title One',
            'children': [
                {
                    'level': 2,
                    'id': 'title-two',
                    'name': 'Title Two',
                    'children': [
                        {
                            'level': 3,
                            'id': 'title-three',
                            'name': 'Title Three',
                            'children': [],
                        },
                    ],
                },
                {
                    'level': 2,
                    'id': 'title-four',
                    'name': 'Title Four',
                    'children': [],
                },
            ],
        },
    ]

