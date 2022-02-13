import re

from spekulatio.exceptions import SpekulatioValueError


class Filetype:
    """A filetype is just a file pattern (in regex form) with a name.

    For example:

        jpeg -> '.(jpeg|jpg)$'
        <underscore_file> -> r'^_.+'

    When defined, a scope can also be provided and it determines if the pattern
    must be applied over either the relative path or the basename of a file in order
    to know if such file is of the given filetype.
    """

    valid_pattern_scopes = ("filename", "relative-path")

    def __init__(self, name, pattern, pattern_scope="relative-path"):

        # set name
        self.name = name

        # set pattern
        try:
            self.pattern = re.compile(pattern)
        except re.error:
            raise SpekulatioValueError(
                f"The provided pattern '{pattern}' is not a valid regular expression."
            )

        # set pattern scope
        if pattern_scope not in self.valid_pattern_scopes:
            valid_pattern_scopes_str = ", ".join(self.valid_pattern_scopes)
            raise SpekulatioValueError(
                f"The scope for the pattern of a filetype must be one of: {valid_pattern_scopes_str}."
                f" Received: '{pattern_scope}'."
            )
        self.pattern_scope = pattern_scope

    def check(self, path):
        """Check if the provided path matches with this filetype.

        The whole path is taken into account not only the basename.
        """
        string = path.name if self.pattern_scope == "filename" else str(path)
        return bool(self.pattern.search(string))

    def __str__(self):
        return f"{self.name}: {self.pattern.pattern}"
