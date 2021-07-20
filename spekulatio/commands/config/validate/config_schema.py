from spekulatio.models.actions import all_actions
from spekulatio.models.actions import action_map_presets

allowed_actions = list(all_actions.keys())
allowed_presets = list(action_map_presets.keys())

config_schema = {
    "filetypes": {
        "type": "list",
        "required": False,
        "empty": False,
        "schema": {
            "type": "dict",
            "schema": {
                "name": {
                    "type": "string",
                    "required": True,
                    "empty": False,
                },
                "extensions": {
                    "type": "list",
                    "excludes": "regex",
                    "required": True,
                    "empty": False,
                    "schema": {
                        "type": "string",
                        "empty": False,
                    },
                },
                "regex": {
                    "type": "string",
                    "excludes": "extensions",
                    "required": True,
                    "empty": False,
                },
                "scope": {
                    "type": "string",
                    "required": False,
                    "empty": False,
                    "allowed": ["filename", "full-path"],
                    "dependencies": "regex",
                },
            },
        },
    },
    "output_dir": {
        "type": "string",
        "required": True,
        "empty": False,
    },
    "input_dirs": {
        "type": "list",
        "required": True,
        "empty": False,
        "schema": {
            "type": "dict",
            "schema": {
                "path": {
                    "type": "string",
                    "required": True,
                    "empty": False,
                },
                "preset": {
                    "type": "string",
                    "required": False,
                    "empty": False,
                    "allowed": allowed_presets,
                },
                "actions": {
                    "type": "list",
                    "required": False,
                    "empty": False,
                    "schema": {
                        "type": "dict",
                        "required": True,
                        "empty": False,
                        "schema": {
                            "filetype": {
                                "type": "string",
                                "required": True,
                                "empty": False,
                            },
                            "action": {
                                "type": "string",
                                "required": True,
                                "empty": False,
                                "allowed": allowed_actions,
                            },
                        },
                    },
                },
                "default_action": {
                    "type": "string",
                    "required": False,
                    "empty": False,
                    "allowed": allowed_actions,
                },
            },
        },
    },
}
