import logging

from .actions import copy


def build_file_tree(src_path, dst_path, no_cache, actions):
    """Build a file tree at dst_path by perfoming a set of actions per file
    type over src_path.

    The files at src_path will be traversed recursively and each one will be
    checked against the available actions. If the file suffix is present in the
    actions map, the function associated to it will be executed.

    Each function must be of the form
    ``func(root_src_path, src_path, root_dst_path, dst_path)``,
    where:

        :root_src_path: is the root of the source file tree
        :src_path: is the path object of the file to be transformed
        :root_dst_path: is the root of the destination file tree
        :dst_path: it the path object of the output file

    The default action for a file is just to be copied over the destination file
    tree without transformation.

    To skip a file just pass an action function that does nothing.

    :param src_path: source directory.
    :param dst_path: destination directory.
    :param no_cache: if False, output files will only be generated if
        the source file is more modern than its destination. If True, all files
        will be generated irrespectively of their timestamp.
    :param actions: map of suffixes and functions. For example::

            {
                '.scss': ('.css', convert_to_css),
                '.pdf': convert_to_html,
            }

        You can pass both a function of a tuple with two elements. If you pass a
        tuple, the first element must be the extension to use in the output file,
        and the second element must be the function itself.

    Output files have the same filename as the input files unless a new extension
    is specified in ``actions``, in which case the stem will be the same but the
    extension will be modified.
    """
    logging.debug(f"- Building from {src_path}")
    _build_file_tree(src_path, dst_path, src_path, no_cache, actions)


def _build_file_tree(root_src_path, root_dst_path, current_dir, no_cache, actions):
    """Process recursively all the directories that hang from current_dir."""
    for src_path in current_dir.iterdir():

        # get path in destination
        relative_src_path = src_path.relative_to(root_src_path)
        dst_path = root_dst_path.joinpath(*relative_src_path.parts)

        if src_path.is_dir():
            # create directory
            logging.debug(f"directory: {dst_path}")
            dst_path.mkdir(parents=True, exist_ok=True)

            # process its children
            _build_file_tree(root_src_path, root_dst_path, src_path, no_cache, actions)
        else:
            # get new suffix and action function
            value = actions.get(relative_src_path.suffix, copy)
            if isinstance(value, (tuple, list)):
                dst_path = dst_path.with_suffix(value[0])
                action = value[1]
            else:
                action = value

            # check age of destination file
            if dst_path.is_file() and no_cache is False:
                dst_timestamp = dst_path.stat().st_mtime
                src_timestamp = src_path.stat().st_mtime
                if dst_timestamp >= src_timestamp:
                    logging.debug(f"(up-to-date): {dst_path}")
                    continue

            # perform action
            logging.debug(f"{action.__name__}: {dst_path}")
            try:
                action(root_src_path, src_path, root_dst_path, dst_path)
            except Exception as err:
                logging.exception(f"Error while processing {src_path}: {err}")

