
category_lookup_table = {
    '.html': 'page',
    '.css': 'style',
    '.js': 'script',
    '.jpeg': 'image',
    '.webp': 'image',
    '.png': 'image',
    '.gif': 'image',
    '.svg': 'image',
}


def get_category(path):
    """Return a normalized category for the given path.

    If the path is a directory, the returned value is: '<dir>'
    If the path is a virtual node, the returned value is: '<virt>'
    If the path is a file of an unknown type, the returned value is '<file>'
    """

    # check if directory
    if path.is_dir():
        return '<dir>'

    # check if virtual node
    if path.name.endswith('.meta.yaml') or path.name.endswith('.meta.yml'):
        return '<virt>'

    # check if normal input file
    return category_lookup_table.get(path.suffix, '<file>')

