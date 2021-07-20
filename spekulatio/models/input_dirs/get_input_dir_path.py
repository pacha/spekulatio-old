from pathlib import Path
from spekulatio.exceptions import SpekulatioConfigError


def get_input_dir_path(path_name, spekulatio_path):
    """Return the path object for a given absolute or relative path name.

    If the path name is relative the actual location of the directory will
    be searched in the spekulatio path.

    If the path name is absolute the function will only check that it
    exists.
    """
    provided_path = Path(path_name)
    for root_path in spekulatio_path:

        # if provided_path is absolute, the result of this operation is just 'path'
        path = root_path / provided_path
        if path.is_dir():
            return path

    raise SpekulatioConfigError(f"'{path_name}' does not exist or not a directory.")
