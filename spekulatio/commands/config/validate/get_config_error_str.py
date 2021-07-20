def get_config_error_str(errors, depth=0):
    """Transform a Cerberus' error dictionary into a human friendly string.

    Depending on the type of each element of the structure this function
    calls itself recursively adding additional indent space at each step.
    """

    # get current indent
    indent = " " * depth

    # get the string depending on the type of the passed parameter
    if isinstance(errors, str):
        error_str = errors
    elif isinstance(errors, dict):
        error_str = ""
        for key, value in errors.items():
            key_str = (
                f"Element at position {key}" if isinstance(key, int) else f"'{key}'"
            )
            error_str += (
                f"\n{indent}{key_str}: {get_config_error_str(value, depth + 1)}"
            )
    elif isinstance(errors, list):
        prefix = "" if len(errors) == 1 else f"\n{indent}"
        error_str = ""
        for error in errors:
            error_str += f"{prefix}{get_config_error_str(error, depth + 1)}"
    else:
        error_str = str(errors)

    return error_str
