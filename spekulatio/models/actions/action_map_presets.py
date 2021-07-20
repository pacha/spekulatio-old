action_map_presets = {
    "base": {
        "actions": [
            {
                "filetype": "<underscore_file>",
                "action": "ignore",
            },
            {
                "filetype": "<virtual_node>",
                "action": "virtual_node",
            },
            {
                "filetype": "<dir>",
                "action": "create_dir",
            },
        ],
    },
    "site_content": {
        "actions": [
            {
                "filetype": "html",
                "action": "html_to_html",
            },
            {
                "filetype": "md",
                "action": "md_to_html",
            },
            {
                "filetype": "rst",
                "action": "rst_to_html",
            },
            {
                "filetype": "json",
                "action": "json_to_html",
            },
            {
                "filetype": "yaml",
                "action": "yaml_to_html",
            },
            {
                "filetype": "sass",
                "action": "sass_to_css",
            },
        ],
        "default_action": "copy",
    },
    "site_templates": {
        "actions": [
            {
                "filetype": "html",
                "action": "use_as_template",
            },
            {
                "filetype": "md",
                "action": "md_to_html",
            },
            {
                "filetype": "rst",
                "action": "rst_to_html",
            },
            {
                "filetype": "json",
                "action": "json_to_html",
            },
            {
                "filetype": "yaml",
                "action": "yaml_to_html",
            },
            {
                "filetype": "sass",
                "action": "sass_to_css",
            },
        ],
        "default_action": "copy",
    },
    "site_data": {
        "default_action": "copy",
    },
}
