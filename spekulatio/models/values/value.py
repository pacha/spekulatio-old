import logging as log

from spekulatio.exceptions import SpekulatioValueError


class Value:
    """A value defined by the user in a frontmatter or _values.yaml file."""

    scopes = [
        "local",
        "level",
        "branch",
        "default",
    ]

    operations = [
        "replace",
        "merge",
        "append",
        "delete",
    ]

    underscore_keys = {
        # input 
        "_template": {"scope": "default", "operation": "replace", "type": str},
        "_alias": {"scope": "local", "operation": "replace", "type": str},
        "_sort": {"scope": "local", "operation": "replace", "type": list},
        "_sort_options": {"scope": "default", "operation": "merge", "type": dict},
        "_jinja_options": {"scope": "default", "operation": "merge", "type": dict},
        "_rst_options": {"scope": "default", "operation": "merge", "type": dict},
        "_md_options": {"scope": "default", "operation": "merge", "type": dict},
        "_sass_options": {"scope": "default", "operation": "merge", "type": dict},

        # output
        "_title": {"scope": "local", "operation": "replace", "type": str},
        "_url": {"scope": "local", "operation": "replace", "type": str},
        "_toc": {"scope": "local", "operation": "replace", "type": list},
        "_content": {"scope": "local", "operation": "replace", "type": str},
        "_src_text": {"scope": "local", "operation": "replace", "type": str},
    }

    output_underscore_keys = [
        "_title",
        "_toc",
        "_content",
    ]

    def __init__(self, key, raw_value):
        """A value defined by the user.

        'key' can have the format:

        * key: normal value
        * _key: value with special meaning in Spekulatio
        * __key: value specified with advanced syntax

        When key is of the form '__key', raw_value must be a dictionary:

            {
                'scope': (local|level|branch|default) [default: branch]
                'operation': (replace|merge|append|delete) [default: replace]
                'value': (the actual value) [mandatory except for 'delete']
            }
        """
        # check if it is key for advanced syntax
        if key.startswith("__"):
            self._validate_two_underscores(key, raw_value)
            self.name = key[2:]
            self.value = raw_value.get("value")
            self.scope = raw_value.get("scope", "branch")
            self.operation = raw_value.get("operation", "replace")
        elif key.startswith("_"):
            self._validate_one_underscore(key, raw_value)
            self.name = key
            self.value = raw_value
            self.scope = self.underscore_keys[key]['scope']
            self.operation = self.underscore_keys[key]['operation']
        else:
            self.name = key
            self.value = raw_value
            self.scope = "branch"
            self.operation = "replace"

    @classmethod
    def get_values_from_dict(cls, dictionary):
        values = {
            'default': [],
            'branch': [],
            'level': [],
            'local': [],
        }
        for key, raw_value in dictionary.items():
            value = cls(key, raw_value)
            values[value.scope].append(value)
        return values

    def _validate_two_underscores(self, key, raw_value):
        if not len(key) > 2:
            raise SpekulatioValueError(f"Invalid key name '{key}'.")
        if not isinstance(raw_value, dict):
            raise SpekulatioValueError(
                f"Key '{key}' starts with two underscores but its value is not a dictionary."
            )
        if "value" in raw_value:
            if "operation" in raw_value and raw_value["operation"] == "delete":
                raise SpekulatioValueError(f"Key '{key}' can't provide a 'value' field when the operation is set to 'delete'.")
        else:
            if "operation" not in raw_value or raw_value["operation"] != "delete":
                raise SpekulatioValueError(f"Key '{key}' must provide a 'value' field.")

        # check scope
        scope = raw_value.get("scope", "branch")
        if scope not in self.scopes:
            valid_scopes = ", ".join(self.scopes)
            raise SpekulatioValueError(
                f"Scope '{scope}' not one of {valid_scopes} in key '{key}'."
            )

        # check operation
        operation = raw_value.get("operation", "replace")
        if operation not in self.operations:
            valid_operations = ", ".join(self.operations)
            raise SpekulatioValueError(
                f"Operation '{operation}' not one of {valid_operations} in key '{key}'."
            )
        if operation != "delete":
            value = raw_value["value"]
            if operation == "merge" and not isinstance(value, dict):
                raise SpekulatioValueError(
                    f"Key '{key}' specifies a merge operation but the value is not a dictionary."
                )
            if operation == "append" and not isinstance(value, list):
                raise SpekulatioValueError(
                    f"Key '{key}' specifies an append operation but the value is not a list."
                )

    def _validate_one_underscore(self, key, raw_value):
        # check length
        if not len(key) > 1:
            raise SpekulatioValueError(f"Invalid key name '{key}'.")

        # check that it is actually one of the special keys
        if key not in self.underscore_keys.keys():
            valid_underscore_keys = ", ".join(self.underscore_keys.keys())
            raise SpekulatioValueError(
                f"Underscore key '{key}' not one of {valid_underscore_keys}."
            )

        # check type
        key_type = self.underscore_keys[key]['type']
        if not isinstance(raw_value, key_type):
            raise SpekulatioValueError(
                f"Underscore key '{key}' must be of type {key_type}."
            )

    def __str__(self):
        return f"Value(name: {self.name}, value: {self.value}, scope: {self.scope}, operation: {self.operation})"
