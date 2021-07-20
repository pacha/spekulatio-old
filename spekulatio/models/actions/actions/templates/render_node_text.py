import traceback

from jinja2 import Template

from spekulatio.exceptions import SpekulatioReadError
from spekulatio.exceptions import SpekulatioWriteError

from .get_globals import get_globals


def render_node_text(node, site):

    # get template text
    template_text = node.data["_src_text"]

    # get options
    jinja_options = node.data.get("_jinja_options", {})

    # get template functions
    template_functions = get_globals(site)

    # get template
    template = Template(template_text, **jinja_options)

    # get content
    try:
        content = template.render(_node=node, **node.data, **template_functions)
    except Exception as err:
        msg = f"{node.src_path}: error while rendering content.\n" f"Traceback:\n"
        traceback_lines = traceback.TracebackException.from_exception(err).format()
        only_template_lines = [line for line in traceback_lines if " template" in line]
        msg = msg + "".join(only_template_lines)
        msg += f"Error ({type(err).__name__}): {err}\n"
        raise SpekulatioWriteError(msg)

    return content
