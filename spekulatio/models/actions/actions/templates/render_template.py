import traceback

from jinja2.exceptions import TemplateNotFound

from spekulatio.exceptions import SpekulatioReadError
from spekulatio.exceptions import SpekulatioWriteError

from .get_env import get_env


def render_template(node, site):

    # get template name
    template_name = node.data.get("_template", "default.html")

    # get environment
    jinja_options = node.data.get("_jinja_options", {})
    jinja_env = get_env(site, jinja_options)

    # get template
    try:
        template = jinja_env.get_template(template_name)
    except TemplateNotFound:
        raise SpekulatioReadError(
            f"{node.src_path}: template '{template_name}' not found."
        )

    # get content
    try:
        content = template.render(_node=node, **node.data)
    except Exception as err:
        msg = (
            f"{node.src_path}: error rendering template '{template_name}'\n"
            f"Traceback:\n"
        )
        traceback_lines = traceback.TracebackException.from_exception(err).format()
        only_template_lines = [line for line in traceback_lines if " template" in line]
        msg = msg + "".join(only_template_lines)
        msg += f"Error: {err}\n"
        raise SpekulatioWriteError(msg)

    return content
