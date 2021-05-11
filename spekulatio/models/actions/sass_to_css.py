
import sass

extension_change = ".css"

def extract(node):
    return {}

def build(src_path, dst_path, node, **kwargs):
    """Compile SCSS into CSS."""

    # get environment for the sass builder
    sass_options = node.data.get('_sass_options', {})
    compile_options = sass_options.get('compile_params', {})

    # get content
    content = sass.compile(filename=str(src_path), **compile_options)

    # write file
    dst_path.write_text(content)

