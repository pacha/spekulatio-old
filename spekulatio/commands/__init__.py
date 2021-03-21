import click

from .build import build
from .serve import serve


@click.group()
def spekulatio():
    pass


spekulatio.add_command(build)
spekulatio.add_command(serve)
