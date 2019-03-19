
def name_sorting(nodes, direction, data):
    """Sort nodes by name."""
    reverse = direction == 'desc'
    return sorted(nodes, reverse=reverse, key=lambda n: str(n))

