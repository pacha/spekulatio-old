import sys
import logging

from pathlib import Path

import click

from spekulatio.som import SOM
from spekulatio.exceptions import SpekulatioError
from spekulatio.build_file_tree import build_file_tree
from spekulatio.build_file_tree.actions import ignore
from spekulatio.build_file_tree.actions import compile_scss
from spekulatio.build_file_tree.actions import render_html_factory


current_dir = Path(__file__).absolute().parent
default_template_path = current_dir / 'default_templates'


@click.command()
@click.option('--build-dir', default='./build',
        help="Directory for output files (default: ./build).")
@click.option('--content-dir', default='./content',
        help="Directory for content files (default: ./content).")
@click.option('--template-dir', default='./templates',
        help="Directory for HTML templates (default: ./templates).")
@click.option('--no-cache', default=True, is_flag=True,
        help="Don't check timestamps. Regenerate all files.")
@click.option('--verbose', default=False, is_flag=True,
        help="Show processing messages.")
def create_site(build_dir, content_dir, template_dir, no_cache, verbose):
    """Create static site from content files using a set of HTML templates."""

    # set logging options
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format='%(levelname)s: %(message)s',
    )

    # set directories
    build_path = Path(build_dir)

    content_path = Path(content_dir)
    if not content_path.is_dir():
        click.echo(f"Directory '{content_path}' not found.")
        sys.exit(-1)

    template_path = Path(template_dir)
    if not template_path.is_dir():
        click.echo(f"Directory '{template_path}' not found.")
        sys.exit(-1)

    template_paths = (default_template_path, template_path)

    try:
        # process file tree in template path
        build_file_tree(template_path, build_path, no_cache,
            actions={
                '.html': ignore,
                '.scss': ('.css', compile_scss),
            }
        )

        # get site object model
        som = SOM(content_path)

        # initialize render action
        render_html = render_html_factory(som, template_paths)

        # process file tree in content path
        build_file_tree(content_path, build_path, no_cache,
            actions={
                '.scss': ('.css', compile_scss),
                '.rst': ('.html', render_html),
                '.json': ('.html', render_html),
                '.yaml': ('.html', render_html),
                '.yml': ('.html', render_html),
                '.html': ('.html', render_html),
                '.htm': ('.html', render_html),
                '.md': ('.html', render_html),
                '.markdown': ('.html', render_html),
            }
        )

    except SpekulatioError as err:
        click.echo(str(err))
        sys.exit(-1)


if __name__ == '__main__':
    create_site()

