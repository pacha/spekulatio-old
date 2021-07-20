from .actions import ignore
from .actions import use_as_template
from .actions import create_dir
from .actions import virtual_node
from .actions import html_to_html
from .actions import md_to_html
from .actions import rst_to_html
from .actions import json_to_html
from .actions import yaml_to_html
from .actions import sass_to_css
from .actions import copy
from .actions import render
from .actions import render_without_frontmatter

all_actions = {
    "ignore": ignore,
    "use_as_template": use_as_template,
    "create_dir": create_dir,
    "virtual_node": virtual_node,
    "html_to_html": html_to_html,
    "md_to_html": md_to_html,
    "rst_to_html": rst_to_html,
    "json_to_html": json_to_html,
    "yaml_to_html": yaml_to_html,
    "sass_to_css": sass_to_css,
    "copy": copy,
    "render": render,
    "render_without_frontmatter": render_without_frontmatter,
}

ignore_actions = [ignore, use_as_template]

from .action_map_presets import action_map_presets
from .action_map import ActionMap
