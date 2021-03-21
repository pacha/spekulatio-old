import http.server
import socketserver

import click


@click.command()
@click.option(
    "-h",
    "--host",
    default="127.0.0.1",
    help="Server host (default: 127.0.0.1)",
)
@click.option(
    "-p",
    "--port",
    type=int,
    default=8000,
    help="Server port (default: 8000)",
)
@click.option(
    "--build-dir",
    default="./build",
    help="Directory to be served (default: ./build).",
)
def serve(host, port, build_dir):
    """Serve site for local development."""

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=build_dir, **kwargs)

    with socketserver.TCPServer((host, port), Handler) as httpd:
        click.echo(f"Serving '{build_dir}' at {host}:{port}...")
        httpd.serve_forever()
