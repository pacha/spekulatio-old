
filetype_lookup_table = {
    '.html': 'html',
    '.htm': 'html',
    '.md': 'md',
    '.mkd': 'md',
    '.mkdn': 'md',
    '.mdwn': 'md',
    '.mdwon': 'md',
    '.markdown': 'md',
    '.rst': 'rst',
    '.json': 'json',
    '.yaml': 'yaml',
    '.yml': 'yaml',
    '.css': 'css',
    '.scss': 'sass',
    '.sass': 'sass',
    '.js': 'js',
    '.jpeg': 'jpeg',
    '.webp': 'webp',
    '.png': 'png',
    '.gif': 'gif',
    '.svg': 'svg',
}


def get_filetype(path):
    """Return a normalized filetype for the given path.

    If the path is a directory, the returned value is: '<dir>'
    If the path is a file of an unknown type, the returned value is '<file>'
    """
    if path.is_dir():
        return '<dir>'

    return filetype_lookup_table.get(path.suffix, '<file>')


