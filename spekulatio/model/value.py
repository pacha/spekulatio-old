import logging as log

from spekulatio.exceptions import SpekulatioValueError


class Value:
    """A value defined by the user in a frontmatter or _values.yaml file."""

    scopes = [
        "local",
        "level",
        "branch",
    ]

    operations = [
        "replace",
        "merge",
        "append",
        "delete",
    ]

    underscore_keys = [
        "_template",
        "_sort",
        "_md_options",
        "_rst_options",
    ]

    def __init__(self, key, raw_value):
        """A value defined by the user.

        'key' can have the format:

        * key: normal value
        * _key: value with special meaning in Spekulatio
        * __key: value specified with advanced syntax

        When key is of the form '__key', raw_value must be a dictionary:

            {
                'scope': (local|level|branch) [default: branch]
                'operation': (replace|merge|append|delete) [default: replace]
                'value': (the actual value) [mandatory]
            }
        """
        # check if it is key for advanced syntax
        if key.startswith("__"):
            self._validate_two_underscores(key, raw_value)
            self.name = key[2:]
            self.value = raw_value["value"]
            self.scope = raw_value.get("scope", "branch")
            self.operation = raw_value.get("operation", "replace")
        elif key.startswith("_"):
            self._validate_one_underscore(key, raw_value)
            self.name = key
            self.value = raw_value
            self.scope = "branch"
            self.operation = "replace"
        else:
            self.name = key
            self.value = raw_value
            self.scope = "branch"
            self.operation = "replace"

    def _validate_two_underscores(self, key, raw_value):
        if not len(key) > 2:
            raise SpekulatioValueError(f"Invalid key name '{key}'.")
        if not isinstance(raw_value, dict):
            raise SpekulatioValueError(
                f"Key '{key}' starts with two underscores but its value is not a dictionary."
            )
        if "value" not in raw_value:
            if "operation" not in raw_value or raw_value["operation"] != "delete":
                raise SpekulatioValueError(f"Key '{key}' must provide a 'value' field.")
        if "scope" in raw_value:
            scope = raw_value["scope"]
            if scope not in self.scopes:
                valid_scopes = ", ".join(self.scopes)
                raise SpekulatioValueError(
                    f"Scope '{scope}' not one of {valid_scopes} in key '{key}'."
                )
        if "operation" in raw_value:
            operation = raw_value["operation"]
            if operation not in self.operations:
                valid_operations = ", ".join(self.operations)
                raise SpekulatioValueError(
                    f"Operation '{operation}' not one of {valid_operations} in key '{key}'."
                )
            value = raw_value["value"]
            if operation == "merge" and not isinstance(value, dict):
                raise SpekulatioValueError(
                    f"Key '{key}' specifies a merge operation but the value is not a dictionary."
                )
            if operation == "append" and not (
                isinstance(value, list) or isinstance(value, tuple)
            ):
                raise SpekulatioValueError(
                    f"Key '{key}' specifies an append operation but the value is not a list."
                )

    def _validate_one_underscore(self, value):
        if not len(key) > 1:
            raise SpekulatioValueError(f"Invalid key name '{key}'.")
        if key not in self.underscore_keys:
            valid_underscore_keys = ", ".join(self.underscore_keys)
            raise SpekulatioValueError(
                f"Underscore key '{key}' not one of {valid_underscore_keys}."
            )

    def __str__(self):
        return f"Value(name: {self.name}, value: {self.value}, scope: {self.scope}, operation: {self.operation})"
