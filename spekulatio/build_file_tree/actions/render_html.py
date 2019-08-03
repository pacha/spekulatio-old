import logging

import jinja2


def render_html_factory(som, template_paths):
    """Create a render function using a som and a list of template dirs.

    :param som: site object model to use as source of contents
    :param template_paths: paths where to find the templates
    """

    def render_html(root_src_path, src_path, root_dst_path, dst_path):

        # get node
        try:
            src_name = str(src_path.relative_to(root_src_path))
            node = som.map[src_name]
        except KeyError:
            logging.debug(f"{src_name} won't generate HTML")
            return

        # initialize templating environment
        loader = jinja2.FileSystemLoader(template_paths, followlinks=True)
        env = jinja2.Environment(loader=loader)
        env.globals.update(get_node=lambda path: som.map[path])

        # create html
        template_name = node.data.get('_template', 'layout.html')
        template = env.get_template(template_name)
        content = template.render(node=node, data=node.data)
        dst_path.write_text(content)

    return render_html

