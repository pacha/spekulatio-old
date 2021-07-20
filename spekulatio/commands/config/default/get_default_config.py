from spekulatio.exceptions import SpekulatioConfigError


def get_default_config(project_path):
    """Provide a default configuration for the current project path."""
    # define default locations
    build_dir = "./build"
    templates_dir = "./templates"
    data_dir = "./data"
    content_dir = "./content"

    # check directory availability
    has_templates = (project_path / templates_dir).is_dir()
    has_data = (project_path / data_dir).is_dir()
    has_content = (project_path / content_dir).is_dir()
    if not any([has_templates, has_data, has_content]):
        raise SpekulatioConfigError(
            "You must provide at least one input directory (eg. './templates', './data', './content') "
            "or provide a Spekulatio configuration file (ie. 'spekulatio.yaml')."
        )

    # generate configuration
    default_config = {
        "output_dir": "build/",
        "input_dirs": [],
    }

    if has_templates:
        default_config["input_dirs"].append(
            {
                "path": "templates/",
                "preset": "site_templates",
            }
        )

    if has_data:
        default_config["input_dirs"].append(
            {
                "path": "data/",
                "preset": "site_data",
            }
        )

    if has_content:
        default_config["input_dirs"].append(
            {
                "path": "content/",
                "preset": "site_content",
            }
        )

    return default_config
