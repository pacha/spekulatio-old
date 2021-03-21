import re
import logging as log

from . import actions
from collections import namedtuple


Rule = namedtuple("Rule", ["filetype", "pattern", "action", "extension_change"])


class ActionMap:
    """Map to match filetypes to actions.

    An ActionMap is assigned to a directory and it determines what should
    be done with each file inside it during the process of building the site.

    In Scaffolding, both template and content directories are assigned an
    ActionMap.
    """

    patterns = {
        "values_file": r"^_values.(yml|yaml)",
        "underscore_file": r"^_",
        "html": r"^.+\.(htm|html)$",
        "rst": r"^.+\.rst$",
        "md": r"^.+\.(md|mkd|mkdn|mdwn|mdown|markdown)$",
        "json": r"^.+\.json$",
        "yaml": r"^.+\.(yml|yaml)$",
        "scss": r"^.+\.scss$",
        "any": r"^.*$",
    }

    actions = {
        "ignore": None,
        "copy": actions.copy,
        "render": actions.render,
        "compile_css": actions.compile_css,
        "process_values": actions.process_values,
    }

    extension_changes = {
        "render": ".html",
        "compile_css": ".scss",
    }

    def __init__(self, rule_definitions):
        """Create an actionmap based on rule definitions.

        A rule definition is a tuple of the format::

            (<filetype>, <action_name>)

        which is converted, using the file patterns, actions and extension
        changes above into into a rule like:

            (<filetype>, <pattern>, <action>, <extension_change>)

        where ``pattern`` is the regex that is used to match that filetype,
        ``action`` is the function to execute for that file and
        ``extension_change`` is the extension of the file generated once the
        action is executed (if None, the generated file will have the same
        extension as the original file).
        """

        self.rules = []

        # populate the rules of the action map
        for rule_definition in rule_definitions:

            # get pattern
            filetype = rule_definition[0]
            try:
                pattern = self.patterns[filetype]
            except KeyError:
                raise ValueError(f"Filetype '{filetype}' not supported by Spekulatio.")

            # get action
            action_name = rule_definition[1]
            try:
                action = self.actions[action_name]
            except KeyError:
                raise ValueError(f"Action '{action_name}' not supported by Spekulatio.")

            # get extension change
            extension_change = self.extension_changes.get(action_name)

            # append rule
            rule = Rule(filetype, pattern, action, extension_change)
            self.rules.append(rule)

    def match(self, filename):
        """Match a filename (basename) against the action map.

        :return: a tuple of the form (action, output_filename)
        """
        for rule in self.rules:
            if re.match(rule.pattern, filename):
                filetype = rule.filetype
                action = rule.action
                extension_change = rule.extension_change
                return filetype, action, extension_change

        return None, None, None
