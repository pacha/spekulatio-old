import logging as log

from spekulatio.exceptions import SpekulatioConfigError
from .read.get_config_content import get_config_content
from .default.get_default_config import get_default_config
from .validate.validate_config import validate_config


def get_config(project_path, config_path):
    """Return the Spekulatio configuration as a dictionary."""
    # get content
    if config_path:
        config_content = get_config_content(config_path)
    else:
        config_content = get_default_config(project_path)

    # validate
    validate_config(config_content)

    return config_content
