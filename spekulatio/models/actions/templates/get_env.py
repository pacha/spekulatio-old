import jinja2
from collections import defaultdict

from .get_globals import get_globals

# environments are computed only once per site for performance reasons
# structure: {<site1-id>: {<option-set-1>: <env-1>}, ...}
cached_envs = defaultdict(dict)

def get_env(site, jinja_options):
    """Initialize templating environment."""

    # cache keys
    site_id = id(site)
    option_set_id = '<default>' if not jinja_options else frozenset(jinja_options.items())

    # return cached environment or create a new one
    try:
        return cached_envs[site_id][option_set_id]
    except KeyError:
        template_dirs = [
            str(template_dir.absolute()) for template_dir in site.template_dirs
        ]
        loader = jinja2.FileSystemLoader(template_dirs, followlinks=True)
        env = jinja2.Environment(loader=loader, **jinja_options)

        # add template functions
        template_functions = get_globals(site)
        env.globals.update(**template_functions)

        # add env to cache
        cached_envs[site_id][option_set_id] = env
        return env

