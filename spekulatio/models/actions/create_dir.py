import yaml

from spekulatio.exceptions import SpekulatioReadError

extension_change = None


def extract(node):
    """Extract data from the '_values.yaml' file associated to a directory."""

    def get_values_file_path(node):
        """Return the path of the _values.y(a)ml file for this node.

        This only applies to directory nodes. If both ``_values.yml``
        and ``_values.yaml`` exist, an error is raised.
        """
        # get paths for both _values.yaml and _values.yml
        full_extension_path = node.src_path / "_values.yaml"
        full_extension_exists = full_extension_path.exists()

        short_extension_path = node.src_path / "_values.yml"
        short_extension_exists = short_extension_path.exists()

        # check presence of the files
        if full_extension_exists and short_extension_exists:
            raise SpekulatioReadError(
                f"{node.relative_src_path}: both _values.yaml and _values.yml found in directory. "
                "Only one is allowed."
            )
        elif full_extension_exists:
            return full_extension_path
        elif short_extension_exists:
            return short_extension_path
        else:
            return None

    # get _values.y(a)ml file path
    values_path = get_values_file_path(node)
    if not values_path:
        return {}

    # get data
    yaml_text = values_path.read_text()
    data = yaml.safe_load(yaml_text) or {}

    return data


def build(src_path, dst_path, node, **kwargs):
    """Create directory"""
    dst_path.mkdir(parents=True, exist_ok=True)
