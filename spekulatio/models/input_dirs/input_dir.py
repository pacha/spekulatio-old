from pathlib import Path

from spekulatio.models.actions import use_as_template
from spekulatio.models.actions import action_map_presets
from spekulatio.models.actions import ActionMap
from spekulatio.models.filetypes import default_filetype_map
from spekulatio.exceptions import SpekulatioConfigError


class InputDir:
    """An InputDir is the combination of a directory path and a set of actions."""

    def __init__(
        self,
        path,
        preset_name=None,
        filetype_map=None,
        action_dicts=None,
        default_action_name=None,
    ):
        # set path
        if not path.is_dir():
            raise SpekulatioConfigError(
                f"The path {path} doesn't exist, it is not readable or not a directory."
            )
        self.path = path

        # setup action map (use default filetype_map if none provided)
        if not filetype_map:
            filetype_map = default_filetype_map
        self.action_map = ActionMap(filetype_map)

        # add actions from preset
        if preset_name:

            # update actions
            preset_action_dicts = action_map_presets[preset_name].get("actions")
            self.action_map.update_actions(preset_action_dicts)

            # update default action
            default_action_name = action_map_presets[preset_name].get("default_action")
            self.action_map.update_default_action(default_action_name)

        # add actions from user
        if action_dicts:
            self.action_map.update_actions(action_dicts)
        if default_action_name:
            self.action_map.update_default_action(default_action_name)

        # add actions from base preset
        # (they override any other action)
        base_action_dicts = action_map_presets["base"].get("actions")
        self.action_map.update_actions(base_action_dicts)

    def is_template_dir(self):
        return use_as_template in self.action_map.map.values()

    def __str__(self):
        return str(self.path)
