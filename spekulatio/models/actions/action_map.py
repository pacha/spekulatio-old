from spekulatio.models.actions import all_actions
from spekulatio.exceptions import SpekulatioConfigError


class ActionMap:
    """An ActionMap associates Filetypes to Actions (many-to-one)."""

    def __init__(self, filetype_map):
        self.filetype_map = filetype_map
        self.map = {}
        self.default_action = all_actions["ignore"]

    def update_actions(self, action_dicts):
        """
        Update the current map with a dictionary that maps filetypes to actions.

        If called multiple times, the last call to this method creates entries
        that have priority over the existing ones.

        :param action_dicts: list of dictionaries of the form::

            [
                {
                    'filetype': '<filetype_name>',
                    'action': '<action_name>',
                },
                ...
            ]

        """
        # check if there's anything to do
        if not action_dicts:
            return

        # get new map
        new_map = {}
        for action_dict in action_dicts:

            # get action
            action_name = action_dict["action"]
            action = all_actions[action_name]

            # check filetype
            filetype_name = action_dict["filetype"]
            if filetype_name not in self.filetype_map.get_filetype_names():
                raise SpekulatioConfigError(
                    f"Filetype '{filetype_name}' is not defined."
                )

            # save entry
            new_map[filetype_name] = action

        # add previous entries
        for key, value in self.map.items():
            if key not in new_map:
                new_map[key] = value

        # swap dictionaries (we don't update the old dictionary to use the insertion
        # order as a way to specify priority)
        self.map = new_map

    def update_default_action(self, default_action_name):
        # check if there's anything to do
        if not default_action_name:
            return

        # update default action
        self.default_action = all_actions[default_action_name]

    def get_action(self, path, relative_path):
        """Return the action associated to a given path.

        The path is provided both as a full one (``path``) or relative (``relative_path``).
        """
        # get filetype
        filetype_name = self.filetype_map.get_filetype_name(path, relative_path)

        # get action
        action = self.map.get(filetype_name, self.default_action)

        return action 
