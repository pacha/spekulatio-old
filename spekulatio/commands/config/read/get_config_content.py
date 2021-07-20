import yaml

from spekulatio.exceptions import SpekulatioConfigError


def get_config_content(config_path):
    """Return the content of the config file as a dictionary."""

    # read file
    try:
        yaml_text = config_path.read_text()
    except FileNotFoundError as err:
        raise SpekulatioConfigError(f"File not found: '{config_path}'")

    # parse content
    try:
        config = yaml.safe_load(yaml_text)
    except yaml.parser.ParserError as err:
        raise SpekulatioConfigError(err)

    return config
