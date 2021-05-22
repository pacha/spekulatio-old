
from collections import namedtuple

from spekulatio.models.actions import copy
from spekulatio.models.actions import create_dir
from spekulatio.models.actions import sass_to_css
from spekulatio.models.actions import html_to_html
from spekulatio.models.actions import md_to_html
from spekulatio.models.actions import rst_to_html
from spekulatio.models.actions import json_to_html
from spekulatio.models.actions import yaml_to_html

_underscore_files = r"^_.+$"
_html_files = r"^.+\.(htm|html)$"

FiletreeConf = namedtuple("FiletreeConf", "template_dir ignore_patterns default_action actions")

data_conf = FiletreeConf(
    template_dir=False,
    ignore_patterns=[
        _underscore_files
    ],
    default_action=copy,
    actions={
        '<dir>': create_dir,
    }
)

template_conf = FiletreeConf(
    template_dir=True,
    ignore_patterns=[
        _underscore_files,
        _html_files,
    ],
    default_action=copy,
    actions={
        'md':  md_to_html,
        'rst':  rst_to_html,
        'json':  json_to_html,
        'yaml':  yaml_to_html,
        'sass': sass_to_css,
        '<dir>': create_dir,
    }
)

content_conf = FiletreeConf(
    template_dir=False,
    ignore_patterns=[
        _underscore_files,
    ],
    default_action=copy,
    actions={
        'html': html_to_html,
        'md':  md_to_html,
        'rst':  rst_to_html,
        'json':  json_to_html,
        'yaml':  yaml_to_html,
        'sass': sass_to_css,
        '<dir>': create_dir,
    }
)

