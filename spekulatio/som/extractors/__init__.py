from .rst_extractor import rst_extractor
from .json_extractor import json_extractor
from .yaml_extractor import yaml_extractor

extractors = {
    '.rst': rst_extractor,
    '.json': json_extractor,
    '.yaml': yaml_extractor,
    '.yml': yaml_extractor,
}

