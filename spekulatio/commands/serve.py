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
@click.argument(
    "directory",
    default="./build",
)
def serve(host, port, directory):
    """Serve site for local development."""

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=directory, **kwargs)

    class Server(socketserver.TCPServer):
        allow_reuse_address = True

    with socketserver.TCPServer((host, port), Handler) as httpd:
        click.echo(f"Serving '{directory}' at {host}:{port}...")
        httpd.serve_forever()
