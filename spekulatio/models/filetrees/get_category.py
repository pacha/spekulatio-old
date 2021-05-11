
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
    If the path is a file of an unknown type, the returned value is '<file>'
    """

    if path.is_dir():
        return '<dir>'

    return category_lookup_table.get(path.suffix, '<file>')

