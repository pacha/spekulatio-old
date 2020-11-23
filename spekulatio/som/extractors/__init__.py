from .rst_extractor import rst_extractor
from .json_extractor import json_extractor
from .yaml_extractor import yaml_extractor
from .html_extractor import html_extractor
from .md_extractor import md_extractor

extractors = {
    '.rst': rst_extractor,
    '.json': json_extractor,
    '.yaml': yaml_extractor,
    '.yml': yaml_extractor,
    '.html': html_extractor,
    '.htm': html_extractor,
    '.md': md_extractor,
    '.markdown': md_extractor,
}

