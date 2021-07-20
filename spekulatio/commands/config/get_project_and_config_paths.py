from pathlib import Path


def get_project_and_config_paths(custom_config_location):
    """Return the actual path of the config file to use."""
    # check if a custom config is provided
    if custom_config_location:
        config_path = Path(custom_config_location)
        if not config_path.is_file():
            raise FileNotFoundError()
        project_path = config_path.parent
        return project_path, config_path

    # check default config files
    project_path = Path.cwd()
    for config_path in (
        project_path / "spekulatio.yaml",
        project_path / "spekulatio.yml",
    ):
        if config_path.is_file():
            return project_path, config_path

    return project_path, None
