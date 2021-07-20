import re

from .filetype import Filetype

from spekulatio.exceptions import SpekulatioValueError


class FiletypeMap:
    """A FiletypeMap is a collection of Filetypes.

    Filetypes can be retrieved using just their name and registered by passing
    a list of extensions or a regex.
    """

    default_pattern_scope = "filename"

    def __init__(self):
        self.map = {}

    def update(self, filetype_dicts):
        """Register multiple filetypes at once.

        This function can be called multiple times and filetype definitions accumulate on each call.
        If a filetype is defined multiple times, the latest definition overwrites the rest.

        :param filetype_dicts: list of dictionaries of the form::

                [
                    {
                        'name': '<filetype_name>',
                        'extensions': ['<file-extension-1>', '<file-extension-2>', ...],
                    },
                    {
                        'name': '<filetype_name>',
                        'regex': '<regex>',
                    },
                    ...
                ]

            For each dictionary in the list, it is possible to specify EITHER the valid extensions of the
            type or a single regex.
        """

        # create map with new filetypes
        new_map = {}
        for filetype_dict in filetype_dicts:

            # get name
            name = filetype_dict["name"]

            # get pattern scope
            scope = filetype_dict.get("scope", self.default_pattern_scope)

            # get pattern
            if "extensions" in filetype_dict:
                extensions = filetype_dict["extensions"]
                pattern = self.get_pattern_from_extensions(extensions)
                if scope != "filename":
                    raise SpekulatioValueError(
                        f"The scope for a filename defined using extensions can "
                        f"only be 'filename' (scope provided: '{scope}')"
                    )
            elif "regex" in filetype_dict:
                pattern = filetype_dict["regex"]

            # create filetype
            filetype = Filetype(name, pattern, scope)
            new_map[name] = filetype

        # add old filetypes
        # (we don't overwrite the old map directly so we can preserve the correct insert order for look-up)
        for name, filetype in self.map.items():
            if name not in new_map:
                new_map[name] = filetype

        # finally, swap dictionaries
        self.map = new_map

    @staticmethod
    def get_pattern_from_extensions(extensions):
        """Create regex expression for a set of file extensions."""
        # ensure that all extensions start with period
        normalized_extensions = [
            f".{extension}" if extension[0] != "." else extension
            for extension in extensions
        ]

        # ensure that no user input is interpreted as a regex special character
        escaped_extensions = [
            re.escape(normalized_extension)
            for normalized_extension in normalized_extensions
        ]

        # build regex
        extension_pattern = "|".join(escaped_extensions)
        pattern = f"^.*({extension_pattern})"
        return pattern

    def get_filetype_name(self, path):
        """Return the filetype of the provided path.

        * If path is a directory, the filetype name will be '<dir>' independently of the registered filetypes.
        * If path does not match any filetype then None is returned.
        """

        # check if directory
        if path.is_dir():
            return "<dir>"

        # check if virtual node or underscore file
        filename = path.name
        if filename.startswith("_"):
            return "<underscore_file>"
        if filename.endswith(".meta.yaml") or filename.endswith(".meta.yml"):
            return "<virtual_node>"

        # use the map to determine the filetype
        for name, filetype in self.map.items():
            if filetype.check(path):
                return filetype.name
        return None

    def get_filetype_names(self):
        """Return all available filetype names."""
        return list(self.map.keys()) + ["<dir>", "<underscore_file>", "<virtual_node>"]
