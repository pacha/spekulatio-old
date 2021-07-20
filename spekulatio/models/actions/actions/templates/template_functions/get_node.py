from spekulatio.exceptions import SpekulatioWriteError


def get_node_factory(site):
    def get_node(url=None, alias=None):
        """Get node using its url or its alias."""
        if url:
            try:
                return site.nodes[url]
            except KeyError:
                raise SpekulatioWriteError(f"Can't find node with url={url}")
        if alias:
            try:
                return site.aliases[alias]
            except KeyError:
                raise SpekulatioWriteError(f"Can't find node with alias={alias}")
        raise SpekulatioWriteError(
            f"'get_node()' must be called passing either an url or an alias."
        )

    return get_node
