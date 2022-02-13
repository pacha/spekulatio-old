from spekulatio.exceptions import SpekulatioWriteError


def get_url_factory(site):
    def get_url(alias):
        """Get url of a node from its alias."""
        try:
            return site.aliases[alias].url
        except KeyError:
            raise SpekulatioWriteError(f"Can't find node with alias={alias}")

    return get_url
