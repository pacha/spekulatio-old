from .template_functions import now_as
from .template_functions import print_as_json
from .template_functions import get_url_factory
from .template_functions import get_node_factory

# globals are computed only once per site for performance reasons
# structure: {<site1-id>: {<global-items-site-1>}, ...}
cached_globals = {}


def get_globals(site):
    site_id = id(site)
    if site_id not in cached_globals:
        cached_globals.update(
            {
                site_id: {
                    "now_as": now_as,
                    "print_as_json": print_as_json,
                    "get_url": get_url_factory(site),
                    "get_node": get_node_factory(site),
                }
            }
        )
    return cached_globals[site_id]
