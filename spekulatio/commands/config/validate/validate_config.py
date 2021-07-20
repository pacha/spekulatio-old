from cerberus import Validator

from spekulatio.exceptions import SpekulatioConfigError
from .get_config_error_str import get_config_error_str
from .config_schema import config_schema


def validate_config(config_content):
    """Raise an exception if the config content is not valid."""
    if not config_content:
        raise SpekulatioConfigError("Empty configuration")

    validator = Validator(config_schema)
    if not validator.validate(config_content):
        error_str = get_config_error_str(validator.errors)
        raise SpekulatioConfigError(error_str)
